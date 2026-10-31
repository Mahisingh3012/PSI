# Agent 2: Rules reader

Read the contract, NDA and any publicity or confidentiality clause FIRST, before any other file. Then read the client's
public footprint and every email about publicity or case studies.

Output JSON only:
{
  "rules": [{"id": "R1", "rule": "...", "source": "[Dnn:Lx-y]"}],          // what may be said, by whom approved, notice period, withdrawal
  "approvers": [{"role": "...", "why": "[Dnn:Lx]"}],                        // who must approve (not just who wants to)
  "terms": [{"term": "...", "category": "client_name|site|person|location|capacity|supplier|code_name|commercial|public_link",
             "banned": true, "safe_replacement": "...", "rule": "R?"}]
}

Include in `terms`: the client's legal and short names, every site and sister site, every state/city, every person on the
client side (they are not ours to name), the client's suppliers, internal code/project names, any exact figure published in
the client's annual report or press, and any phrase from the client's public posts that would let a reader match the
case study to that post. Mark the vendor's own staff `banned: false` unless the contract says otherwise.
