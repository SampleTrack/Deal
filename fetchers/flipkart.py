"""
fetchers/flipkart.py - Fetch deals from Flipkart Affiliate API
"""

import logging
import aiohttp
from config import Config

logger = logging.getLogger(__name__)


class FlipkartFetcher:

    BASE_URL = "https://affiliate-api.flipkart.net/affiliate/offers/v1/deals/json"

    CATEGORY_MAP = {
        "electronics": "ELECTRONICS",
        "fashion":     "CLOTHING",
        "skincare":    "BEAUTY_AND_PERSONAL_CARE",
        "home":        "HOME_KITCHEN",
    }

    async def fetch_deals(self, category: str, count: int = 10) -> list:
        """Fetch deals from Flipkart Affiliate API"""
        try:
            fk_category = self.CATEGORY_MAP.get(category, "ELECTRONICS")

            headers = {
                "Fk-Affiliate-Id":    Config.FLIPKART_AFFILIATE_ID,
                "Fk-Affiliate-Token": Config.FLIPKART_AFFILIATE_TOKEN,
            }

            params = {
                "category": fk_category,
                "count":    count,
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.BASE_URL,
                    headers=headers,
                    params=params
                ) as resp:
                    if resp.status != 200:
                        logger.warning(f"Flipkart API returned {resp.status}")
                        return []
                    data = await resp.json()

            return self._parse_results(data, category)

        except Exception as e:
            logger.error(f"Flipkart fetch error: {e}")
            return []

    def _parse_results(self, data: dict, category: str) -> list:
        """Parse Flipkart API response into standard deal format"""
        deals  = []
        items  = data.get("dealsResponse", {}).get("dealDetails", [])

        for item in items:
            try:
                product_info = item.get("productBaseInfoV1", {})
                price_info   = product_info.get("flipkartSellingPrice", {})
                mrp_info     = product_info.get("maximumRetailPrice", {})

                product_id   = product_info.get("productId", "")
                title        = product_info.get("title", "")
                price        = float(price_info.get("amount", 0))
                mrp          = float(mrp_info.get("amount", 0))
                saving       = round(mrp - price, 2) if mrp > price else 0
                discount     = round((saving / mrp) * 100) if mrp > 0 else 0

                rating       = float(product_info.get("averageRating", 0))
                review_count = int(product_info.get("totalNoOfReviews", 0))

                image        = product_info.get("imageUrls", {}).get("400x400", "")

                # Build affiliate URL
                raw_url      = product_info.get("productUrl", "")
                url          = f"{raw_url}&affid={Config.FLIPKART_AFFILIATE_ID}"

                # Filter by minimum quality
                if rating < Config.MIN_RATING:
                    continue
                if review_count < Config.MIN_REVIEWS:
                    continue

                deals.append({
                    "product_id":    product_id,
                    "title":         title,
                    "platform":      "Flipkart",
                    "category":      category,
                    "price":         price,
                    "mrp":           mrp,
                    "saving":        saving,
                    "discount":      discount,
                    "rating":        rating,
                    "review_count":  review_count,
                    "free_delivery": True,   # Flipkart usually offers free delivery
                    "emi":           price > 3000,  # EMI usually available above ₹3000
                    "image":         image,
                    "url":           url,
                    "stock_message": "",
                })

            except Exception as e:
                logger.warning(f"Skipping Flipkart item: {e}")
                continue

        return deals
