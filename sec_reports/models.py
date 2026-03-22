from dataclasses import dataclass


@dataclass
class Company:
    name: str
    ticker: str


@dataclass
class FilingInfo:
    company: Company
    cik: str
    form: str
    filing_date: str
    accession_number: str
    primary_document: str
    document_url: str
