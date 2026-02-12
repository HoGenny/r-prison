from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gacha import GachaBox, GachaBoxRate
from app.models.slime import Slime


BOX_SEEDS: list[dict[str, object]] = [
    {"code": "basic", "name": "Basic Box", "price_rp": 100, "min_rarity": None},
    {"code": "silver", "name": "Silver Box", "price_rp": 300, "min_rarity": "uncommon"},
    {"code": "gold", "name": "Gold Box", "price_rp": 800, "min_rarity": "rare"},
    {"code": "crystal", "name": "Crystal Box", "price_rp": 1500, "min_rarity": "epic"},
]

BOX_RATE_SEEDS: dict[str, list[tuple[str, int]]] = {
    "basic": [
        ("common", 7000),
        ("uncommon", 2300),
        ("rare", 600),
        ("epic", 90),
        ("legendary", 10),
    ],
    "silver": [
        ("common", 0),
        ("uncommon", 8000),
        ("rare", 1700),
        ("epic", 270),
        ("legendary", 30),
    ],
    "gold": [
        ("common", 0),
        ("uncommon", 0),
        ("rare", 8500),
        ("epic", 1300),
        ("legendary", 200),
    ],
    "crystal": [
        ("common", 0),
        ("uncommon", 0),
        ("rare", 0),
        ("epic", 9000),
        ("legendary", 1000),
    ],
}

SLIME_SEEDS: list[dict[str, object]] = [
    {"name": "Study Sprout", "rarity": "common", "element": "study", "description": "Learns from every note.", "base_hatch_days": 1},
    {"name": "Desk Hopper", "rarity": "common", "element": "study", "description": "Jumps between to-do lists.", "base_hatch_days": 1},
    {"name": "Squat Blob", "rarity": "common", "element": "exercise", "description": "Gets stronger with reps.", "base_hatch_days": 1},
    {"name": "Plank Puff", "rarity": "common", "element": "exercise", "description": "Steady and balanced.", "base_hatch_days": 1},
    {"name": "Mop Drop", "rarity": "common", "element": "cleanup", "description": "Loves clean floors.", "base_hatch_days": 1},
    {"name": "Wipe Wisp", "rarity": "common", "element": "cleanup", "description": "Clears dusty corners.", "base_hatch_days": 1},
    {"name": "Sleepy Note", "rarity": "common", "element": "study", "description": "Nap first, focus later.", "base_hatch_days": 1},
    {"name": "Focus Pebble", "rarity": "common", "element": "study", "description": "Small but persistent.", "base_hatch_days": 1},
    {"name": "Sprint Gel", "rarity": "uncommon", "element": "exercise", "description": "Likes interval training.", "base_hatch_days": 2},
    {"name": "Tidy Ripple", "rarity": "uncommon", "element": "cleanup", "description": "Makes routines smooth.", "base_hatch_days": 2},
    {"name": "Memo Mist", "rarity": "uncommon", "element": "study", "description": "Stores quick ideas.", "base_hatch_days": 2},
    {"name": "Routine Bud", "rarity": "uncommon", "element": "study", "description": "Grows with consistency.", "base_hatch_days": 2},
    {"name": "Calm Bubble", "rarity": "uncommon", "element": "cleanup", "description": "Keeps spaces serene.", "base_hatch_days": 2},
    {"name": "Scholar Slime", "rarity": "rare", "element": "study", "description": "Masters difficult topics.", "base_hatch_days": 3},
    {"name": "Circuit Slime", "rarity": "rare", "element": "exercise", "description": "Turns sweat into power.", "base_hatch_days": 3},
    {"name": "Prism Slime", "rarity": "rare", "element": "cleanup", "description": "Brightens every room.", "base_hatch_days": 3},
    {"name": "Zen Slime", "rarity": "rare", "element": "study", "description": "Focused under pressure.", "base_hatch_days": 3},
    {"name": "Aurora Mentor", "rarity": "epic", "element": "study", "description": "Guides long-term growth.", "base_hatch_days": 7},
    {"name": "Titan Coach", "rarity": "epic", "element": "exercise", "description": "Pushes limits safely.", "base_hatch_days": 7},
    {"name": "Chrono Sovereign", "rarity": "legendary", "element": "study", "description": "Rules over daily rhythm.", "base_hatch_days": 30},
]


class SeedService:
    async def seed_defaults(self, db: AsyncSession) -> None:
        try:
            await self._seed_boxes(db)
            await self._seed_slimes(db)
            await db.flush()
            await self._seed_box_rates(db)
            await db.commit()
        except IntegrityError:
            await db.rollback()

    async def _seed_boxes(self, db: AsyncSession) -> None:
        existing_codes = set((await db.execute(select(GachaBox.code))).scalars().all())
        for payload in BOX_SEEDS:
            code = payload["code"]
            if isinstance(code, str) and code not in existing_codes:
                db.add(GachaBox(**payload))

    async def _seed_slimes(self, db: AsyncSession) -> None:
        slime_count = await db.scalar(select(func.count()).select_from(Slime))
        if slime_count and slime_count > 0:
            return

        db.add_all([Slime(**payload) for payload in SLIME_SEEDS])

    async def _seed_box_rates(self, db: AsyncSession) -> None:
        box_rows = await db.execute(select(GachaBox.id, GachaBox.code))
        box_ids_by_code: dict[str, int] = {code: box_id for box_id, code in box_rows.all()}

        existing_rows = await db.execute(select(GachaBoxRate.box_id, GachaBoxRate.rarity))
        existing_keys = {(box_id, rarity) for box_id, rarity in existing_rows.all()}

        for code, rates in BOX_RATE_SEEDS.items():
            box_id = box_ids_by_code.get(code)
            if box_id is None:
                continue

            for rarity, weight in rates:
                key = (box_id, rarity)
                if key in existing_keys:
                    continue

                db.add(GachaBoxRate(box_id=box_id, rarity=rarity, weight=weight))


seed_service = SeedService()
