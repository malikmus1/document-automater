import requests

from .models import Company, FilingInfo

_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"


def get_latest_10k(cik: str, company: Company, session: requests.Session) -> FilingInfo:
    """
    Fetch the latest exact 10-K filing (excludes 10-K/A amendments)
    for the given CIK from the EDGAR submissions API.
    """
    resp = session.get(_SUBMISSIONS_URL.format(cik=cik), timeout=30)
    resp.raise_for_status()

    recent = resp.json()["filings"]["recent"]
    forms = recent["form"]
    accessions = recent["accessionNumber"]
    dates = recent["filingDate"]
    primary_docs = recent["primaryDocument"]

    for i, form in enumerate(forms):
        if form == "10-K":  # exact match — excludes 10-K/A amendments
            accession = accessions[i]
            accession_nodashes = accession.replace("-", "")
            numeric_cik = str(int(cik))  # strip leading zeros for archive URL
            doc_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{numeric_cik}/{accession_nodashes}/{primary_docs[i]}"
            )
            return FilingInfo(
                company=company,
                cik=cik,
                form=form,
                filing_date=dates[i],
                accession_number=accession,
                primary_document=primary_docs[i],
                document_url=doc_url,
            )

    raise ValueError(f"No 10-K filing found for {company.name} (CIK {cik})")
