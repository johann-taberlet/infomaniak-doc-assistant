# Understanding k Drive data security

Source: https://www.infomaniak.com/en/support/faq/2462/understanding-kdrive-data-security

---

This guide details the measures implemented by Infomaniak to secure all your data in [k Drive](https://infomaniak.com/gtl/kdrive), whether personal (medical data, identification or login information) or even sensitive (financial information, trade secrets, intellectual property information, research and development, etc.).

## Data security and confidentiality

The k Drive infrastructure consists of several services and servers based on different technologies. The content and structure of each client's content are systematically encrypted and permanently saved in at least 3 locations in several data centers controlled by Infomaniak. Data is stored and processed exclusively in data centers located in Switzerland. Tier III+ data centers guarantee high availability and N+1 redundancy for its critical components.

Storage is performed via Swift, a distributed and highly available cloud data storage technology.

k Drive integrates several levels of protection to protect files:

1. To protect data in transit, the use of the SSL/TLS encryption protocol.
2. To protect saved data, AES 128-bit encryption (AES-128-CBC) with an individual and unique key per k Drive space.

Infomaniak regularly tests k Drive applications and infrastructure to identify potential security vulnerabilities they may have, thereby strengthening security and ensuring protection against attacks.

### But also…

- k Drive offers a data access log and an action history can be viewed directly from the Manager; it is possible to access an [activity report](https://www.infomaniak.com/en/support/faq/2579) to monitor the action history of all your k Drive users; you can also track your data and changes made to each document, spreadsheet, or presentation.
- Only people with a link to public files can view them.
- [Two-step verification](https://www.infomaniak.com/en/support/faq/1940) provides an additional level of security when logging in; if you use two-step verification, you can choose, for example, authentication via the [k Auth application](https://www.infomaniak.com/en/support/faq/2359).
- Refer to [this other guide](https://www.infomaniak.com/en/support/faq/2412) if you are looking for information on data analysis.