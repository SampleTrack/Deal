"""
fetchers/nykaa.py - Fetch deals from Nykaa Affiliate API
Used only for Skincare channel
"""

import logging
import aiohttp
from config import Config

logger = logging.getLogger(__name__)


class NykaaFetcher:

    # Nykaa affiliate API endpoint (check your affiliate dashboard for exact URL)
    BASE_URL = "https://www.nykaa.com/api/affiliate/deals"

    async def fetch_deals(self, category: str = "skincare", count: int = 10) -> list:
        """Fetch skincare/beauty deals from Nykaa"""
        try:
            headers = {
                "affiliate-id": Config.NYKAA_AFFILIATE_ID,
                "Content-Type": "application/json",
            }

            params = {
                "category": "skincare",
                "limit":    count,
                "sort":     "discount",  # sort by highest discount
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.BASE_URL,
                    headers=headers,
                    params=params
                ) as resp:
                    if resp.status != 200:
                        logger.warning(f"Nykaa API returned {resp.status}")
                        return []
                    data = await resp.json()

            return self._parse_results(data)

        except Exception as e:
            logger.error(f"Nykaa fetch error: {e}")
            return []

    def _parse_results(self, data: dict) -> list:
        """Parse Nykaa API response"""
        deals = []
        items = data.get("products", [])

        for item in items:
            try:
                product_id   = str(item.get("id", ""))
                title        = item.get("name", "")
                price        = float(item.get("offer_price", 0))
                mrp          = float(item.get("mrp", 0))
                saving       = round(mrp - price, 2) if mrp > price else 0
                discount     = round((saving / mrp) * 100) if mrp > 0 else 0

                rating       = float(item.get("average_rating", 0))
                review_count = int(item.get("rating_count", 0))
                image        = item.get("image_url", "")

                # Build affiliate URL
                slug         = item.get("slug", "")
                url          = f"https://www.nykaa.com/p/{slug}?utm_source=affiliate&utm_medium={Config.NYKAA_AFFILIATE_ID}"

                if rating < Config.MIN_RATING:
                    continue
                if review_count < Config.MIN_REVIEWS:
                    continue

                deals.append({
                    "product_id":    f"nykaa_{product_id}",
                    "title":         title,
                    "platform":      "Nykaa",
                    "category":      "skincare",
                    "price":         price,
                    "mrp":           mrp,
                    "saving":        saving,
                    "discount":      discount,
                    "rating":        rating,
                    "review_count":  review_count,
                    "free_delivery": price > 499,  # Nykaa free delivery above ₹499
                    "emi":           False,
                    "image":         image,
                    "url":           url,
                    "stock_message": "",
                })

            except Exception as e:
                logger.warning(f"Skipping Nykaa item: {e}")
                continue

        return deals
