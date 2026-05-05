"""
fetchers/amazon.py - Fetch deals from Amazon Product Advertising API
"""

import logging
import hmac
import hashlib
import datetime
import urllib.parse
import aiohttp
from config import Config

logger = logging.getLogger(__name__)


class AmazonFetcher:

    BASE_URL = "https://webservices.amazon.in/paapi5/searchitems"

    # Category → Amazon search index + keywords
    CATEGORY_MAP = {
        "electronics": {"searchIndex": "Electronics",    "keywords": "best seller electronics"},
        "fashion":     {"searchIndex": "Fashion",        "keywords": "trending fashion deals"},
        "skincare":    {"searchIndex": "Beauty",         "keywords": "skincare beauty deals"},
        "home":        {"searchIndex": "HomeImprovement","keywords": "home kitchen appliances deals"},
    }

    async def fetch_deals(self, category: str, count: int = 10) -> list:
        """Fetch deals for a specific category from Amazon PA API"""
        try:
            cat = self.CATEGORY_MAP.get(category, self.CATEGORY_MAP["electronics"])
            payload = {
                "Keywords":        cat["keywords"],
                "SearchIndex":     cat["searchIndex"],
                "ItemCount":       count,
                "PartnerTag":      Config.AMAZON_AFFILIATE_TAG,
                "PartnerType":     "Associates",
                "Marketplace":     "www.amazon.in",
                "Resources": [
                    "ItemInfo.Title",
                    "Offers.Listings.Price",
                    "Offers.Listings.SavingBasis",
                    "Offers.Listings.DeliveryInfo.IsFreeShippingEligible",
                    "Offers.Listings.PaymentInfo.InstallmentInfo",
                    "CustomerReviews.StarRating",
                    "CustomerReviews.Count",
                    "Images.Primary.Large",
                    "Offers.Listings.Availability.Message",
                ]
            }

            # NOTE: Full AWS Signature V4 signing required for production
            # See: https://webservices.amazon.com/paapi5/documentation/
            # For testing use amazon-paapi Python library:
            # pip install amazon-paapi5

            headers = {
                "Content-Type":  "application/json; charset=utf-8",
                "X-Amz-Target":  "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.BASE_URL,
                    json=payload,
                    headers=headers
                ) as resp:
                    if resp.status != 200:
                        logger.warning(f"Amazon API returned {resp.status}")
                        return []
                    data = await resp.json()

            return self._parse_results(data, category)

        except Exception as e:
            logger.error(f"Amazon fetch error: {e}")
            return []

    def _parse_results(self, data: dict, category: str) -> list:
        """Parse Amazon API response into standard deal format"""
        deals = []
        items = data.get("SearchResult", {}).get("Items", [])

        for item in items:
            try:
                title    = item["ItemInfo"]["Title"]["DisplayValue"]
                asin     = item["ASIN"]
                url      = f"https://www.amazon.in/dp/{asin}?tag={Config.AMAZON_AFFILIATE_TAG}"

                listing  = item.get("Offers", {}).get("Listings", [{}])[0]
                price    = listing.get("Price", {}).get("Amount", 0)
                mrp      = listing.get("SavingBasis", {}).get("Amount", 0)
                saving   = round(mrp - price, 2) if mrp > price else 0
                discount = round((saving / mrp) * 100) if mrp > 0 else 0

                # Only show free delivery if actually true
                free_del = listing.get("DeliveryInfo", {}).get("IsFreeShippingEligible", False)

                # Only show EMI if actually available
                emi      = listing.get("PaymentInfo", {}).get("InstallmentInfo") is not None

                reviews  = item.get("CustomerReviews", {})
                rating   = reviews.get("StarRating", {}).get("Value", 0)
                review_count = reviews.get("Count", {}).get("Value", 0)

                image    = item.get("Images", {}).get("Primary", {}).get("Large", {}).get("URL", "")

                stock_msg = listing.get("Availability", {}).get("Message", "")

                # Filter by minimum quality
                if rating < Config.MIN_RATING:
                    continue
                if review_count < Config.MIN_REVIEWS:
                    continue

                deals.append({
                    "product_id":    asin,
                    "title":         title,
                    "platform":      "Amazon",
                    "category":      category,
                    "price":         price,
                    "mrp":           mrp,
                    "saving":        saving,
                    "discount":      discount,
                    "rating":        rating,
                    "review_count":  review_count,
                    "free_delivery": free_del,
                    "emi":           emi,
                    "image":         image,
                    "url":           url,
                    "stock_message": stock_msg,
                })

            except Exception as e:
                logger.warning(f"Skipping item: {e}")
                continue

        return deals
