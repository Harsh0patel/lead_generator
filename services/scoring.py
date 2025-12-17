class Stage3:
    def __init__(self):
        pass

    def scoring(self, df):

        def calculate_score(row):
            score = 0

            # Role Fit
            role_keywords = ["toxicology", "safety", "hepatic", "3d"]
            title = str(row.get("title", "")).lower()
            if any(k in title for k in role_keywords):
                score += 30

            # Funding
            if row.get("funding_stage") in ["Series A", "Series B"]:
                score += 20

            # Biotech Hub
            if row.get("is_biotech_hub") is True:
                score += 10

            # Location Hub
            if row.get("location") in [
                "Boston/Cambridge",
                "Bay Area",
                "Basel",
                "UK Golden Triangle"
            ]:
                score += 10

            # Scientific Intent
            publication_keywords = ["drug-induced liver injury", "liver injury"]
            publication = str(row.get("recent_publication", "")).lower()
            if (
                any(k in publication for k in publication_keywords)
                and row.get("publication_year") in [2023, 2024, 2025]
            ):
                score += 40

            return score

        df["raw_score"] = df.apply(calculate_score, axis=1)

        MAX_SCORE = 110
        df["probability_score"] = (
            df["raw_score"] / MAX_SCORE * 100
        ).clip(upper=100)

        return df
