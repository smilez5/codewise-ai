# CodeWise AI v0.5 — GitHub Pages starter

Shopping-first static website, based on recovered v0.4 HTML. Offers in the interface are demo data until the official eBay Browse API importer successfully runs.

## Publish
1. Upload all files and folders to the root of a public GitHub repository, including `.github/workflows/update-offers.yml`.
2. GitHub Settings > Pages > Deploy from a branch > `main` > `/(root)` > Save.
3. Open the resulting GitHub Pages URL and check the shopping app.

## Enable eBay listing feed
1. Obtain eBay Developer Program production application credentials and required Browse API permissions.
2. Under Settings > Secrets and variables > Actions, create repository secrets `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET`. Never add secrets to files or Pages.
3. Under Settings > Actions > General > Workflow permissions, select **Read and write permissions** if required to allow the workflow to commit the refreshed JSON feed.
4. Under Actions > Refresh eBay offers > Run workflow, run manually and check its log. The workflow also runs daily (GitHub schedules may be delayed).
5. On the site, choose **Offer database** > **Load approved feed**. This feed is initially empty until a successful API refresh.

The importer filters fixed-price listings with an original-price comparison returned by eBay. These are listing discounts, **not coupons** or guaranteed savings. Prices can change. No scraping, checkout automation, affiliate program, or live AI API is included. Before wider launch, add privacy/disclosure information and review eBay's API usage terms.
