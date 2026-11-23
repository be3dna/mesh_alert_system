from enum import StrEnum


class ProposalStatus(StrEnum):
    PROPOSED = "proposed"
    DRAFT = "draft"
    REVIEWED = "reviewed"
    REJECTED = "rejected"
