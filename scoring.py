import re
from typing import List, Tuple

def score_meeting_minutes(content: str) -> Tuple[int, List[str]]:
    score = 0
    reasons = []

    if re.search(r'\b(action items?|decisions? made)\b', content, re.IGNORECASE):
        score += 10
        reasons.append("Contains action items or decisions made (+10)")

    if re.search(r'\b(budget|financial|resource allocation)\b', content, re.IGNORECASE):
        score += 10
        reasons.append("Discusses budget, financial matters, or resource allocation (+10)")

    if re.search(r'\b(educational programs?|policies|curriculum)\b', content, re.IGNORECASE):
        score += 10
        reasons.append("References educational programs, policies, or curriculum (+10)")

    if re.search(r'\b(staff appointments?|resignations?|personnel matters)\b', content, re.IGNORECASE):
        score += 10
        reasons.append("Mentions staff appointments, resignations, or personnel matters (+10)")

    if re.search(r'\b(The Board approved|Motion carried|Resolution adopted)\b', content):
        score += 10
        reasons.append("Uses phrases like 'The Board approved...', 'Motion carried...', 'Resolution adopted...' (+10)")

    if re.search(r'\b(Ayes?:.+Noes?:.+Abstain?:.+)\b', content):
        score += 10
        reasons.append("Records votes (+10)")

    if re.search(r'\b(parliamentary procedure|Robert\'s Rules of Order)\b', content, re.IGNORECASE):
        score += 10
        reasons.append("References parliamentary procedure or Robert's Rules of Order (+10)")

    if re.search(r'\b(Meeting|Minutes)\b', content, re.IGNORECASE):
        score += 5
        reasons.append("Title contains 'Meeting' or 'Minutes' (+5)")

    if re.search(r'\b(\d{1,2}/\d{1,2}/\d{2,4}|\w+ \d{1,2}, \d{4})\b', content):
        score += 5
        reasons.append("Contains date of meeting (+5)")

    if re.search(r'\b(Members Present|Members Absent|Board Members)\b', content, re.IGNORECASE):
        score += 5
        reasons.append("Lists names of board members present/absent (+5)")

    sections = [
        (r'\bCall to Order\b', "Call to Order"),
        (r'\bApproval of Agenda\b', "Approval of Agenda"),
        (r'\bPublic Comments?\b', "Public Comments section"),
        (r'\bAdjournment\b', "Adjournment"),
        (r'\b(Consent Calendar|Action Items|Discussion Items)\b', "Consent Calendar, Action Items, or Discussion Items")
    ]

    for pattern, section_name in sections:
        if re.search(pattern, content, re.IGNORECASE):
            score += 2
            reasons.append(f"Contains {section_name} section (+2)")

    if re.search(r'\b([IVX]+\.|\d+\.)', content):
        score += 2
        reasons.append("Uses numbered/lettered sections and subsections (+2)")

    if len(set(re.findall(r'\n(.{5})', content))) < 10:
        score += 3
        reasons.append("Shows consistent formatting throughout document (+3)")

    if re.search(r'\b(educational outcomes|student achievement|school performance)\b', content, re.IGNORECASE):
        score += 5
        reasons.append("Discusses educational outcomes, student achievement, or school performance (+5)")

    if re.search(r'\b(community engagement|parent involvement|public input)\b', content, re.IGNORECASE):
        score += 5
        reasons.append("References community engagement, parent involvement, or public input (+5)")

    if re.search(r'\b(long-term planning|strategic goals|vision for the school district)\b', content, re.IGNORECASE):
        score += 5
        reasons.append("Discusses long-term planning, strategic goals, or vision for the school district (+5)")

    non_minutes_pages = len(re.findall(r'\n\s*\n', content)) // 25
    if non_minutes_pages > 0:
        penalty = min(non_minutes_pages * 15, score)
        score -= penalty
        reasons.append(f"Penalty for {non_minutes_pages} pages of non-minutes content (-{penalty})")

    if not re.search(r'\b(vote|approved|adopted|carried)\b', content, re.IGNORECASE):
        penalty = min(10, score)
        score -= penalty
        reasons.append(f"Penalty for absence of voting or decision-making language (-{penalty})")

    score = max(0, min(score, 100))
    return score, reasons
