# SE-_LAB1_PES1UG24AM477_13
Patient Health Record Consent Management System . Problem Context &amp; Overview A patient-centric electronic health data gateway where patients explicitly manage granular, time-bound consent permissions for clinics, diagnostic labs, and consulting doctors to access their medical history. Target Stakeholders / Actors: Patient, Clinic Administrator



# Patient Health Record Consent Management System

**Course:** Software Engineering Lab (Lab 1)[cite: 1, 2]  
**Topic:** Requirements Engineering & UML Use-Case Modelling[cite: 1, 2]  
**Problem Statement #13:** Healthcare & Telemedicine[cite: 1]  

---

## 1. Project Overview
A patient-centric electronic health data gateway where patients explicitly manage granular, time-bound consent permissions for clinics, diagnostic labs, and consulting doctors to access their medical history[cite: 1]. The system enforces fine-grained access control, real-time revocation, and strict audit logging to guarantee patient privacy and data sovereignty[cite: 1].

### Target Stakeholders & Actors
* **Patient:** Primary user who grants, views, and revokes access to personal diagnostic records[cite: 1, 2].
* **Clinic Administrator:** Verifies credentials and onboards medical personnel and clinics[cite: 1, 2].
* **Consulting Doctor / Clinic:** Requests and queries patient records within an active, authorized consent window[cite: 1].

---

## 2. Requirements Specification

### Functional Requirements (FR)
| Req ID | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **FR-001**[cite: 1] | The system shall allow patients to grant time-bounded (e.g., 24-hour) access permissions for specific diagnostic records to verified clinic doctors[cite: 1]. | High[cite: 1] | **Pass:** Clinic access automatically revokes upon expiry timestamp[cite: 1].<br>**Fail:** Clinic accesses records after consent expiration[cite: 1]. | Core functionality enabling patient-centric, secure data sharing[cite: 1]. |
| **FR-002** | The system shall allow a patient to manually revoke any active consent permission before the scheduled expiration time. | High[cite: 2] | **Pass:** A doctor's request returns an immediate 403 Forbidden upon revocation.<br>**Fail:** Doctor retains access after revocation. | Enforces patient autonomy and immediate control over sensitive medical records[cite: 1]. |
| **FR-003** | The system shall allow clinic administrators to verify and approve registered medical staff credentials before granting them access to request patient records. | Medium[cite: 2] | **Pass:** Unverified medical staff cannot initiate consent requests or receive access.<br>**Fail:** Unverified practitioner accesses patient data. | Protects patient privacy by preventing unauthorized or fraudulent access[cite: 1]. |
| **FR-004** | The system shall provide patients with an active consent dashboard displaying the real-time status (Active, Expired, Revoked) of all permission grants. | Medium[cite: 2] | **Pass:** Dashboard updates within 1 second of status change showing accurate timestamps.<br>**Fail:** Revoked or expired grants remain marked as active. | Provides transparency and full visibility to patients over their data lifecycle[cite: 1]. |
| **FR-005** | The system shall enforce granular categorization filters, allowing patients to select specific record types (e.g., Blood Reports, Imaging) to share while excluding others. | High[cite: 2] | **Pass:** A doctor granted access to Lab Reports receives an access denied error when attempting to fetch Cardiology reports.<br>**Fail:** All record types are exposed regardless of selected categories. | Prevents over-exposure of sensitive and unrelated medical history[cite: 1]. |

### Non-Functional Requirements (NFR)
| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NFR-001**[cite: 1] | Security & Audit[cite: 1] | All consent grant, revoke, and access events shall be permanently written to an append-only audit trail[cite: 1]. | High[cite: 2] | **Pass:** Benchmarking tests confirm target latency and security standards under simulated peak load with zero log mutability[cite: 1].<br>**Fail:** Any consent event fails to generate an immutable log entry[cite: 1]. | Guarantees non-repudiation and strict compliance with health data privacy regulations[cite: 1]. |
| **NFR-002**[cite: 1] | Performance[cite: 1] | The system shall validate consent authorization tokens and return an access decision in under 200 ms under a concurrent load of 1,000 requests. | High[cite: 2] | **Pass:** 95th percentile response latency is $\le 200\text{ ms}$ under simulated load testing.<br>**Fail:** Response latency exceeds $200\text{ ms}$ or the authorization gateway times out. | Ensures healthcare professionals can access time-critical patient data without latency bottlenecks. |

---

## 3. UML Use-Case Model

### Primary Relationships
* **`UC-01: Grant Granular Consent`** `«include»` $\rightarrow$ **`UC-06: Log Audit Trail`**[cite: 1, 2]
* **`UC-05: Access Diagnostic Records`** `«include»` $\rightarrow$ **`UC-08: Validate Consent Token`**[cite: 2]
* **`UC-07: Set Custom Expiration Window`** `«extend»` $\rightarrow$ **`UC-01: Grant Granular Consent`**[cite: 1, 2]

---

## 4. Repository Structure
```text
.
├── README.md                          # Project overview and requirements specification
├── Requirements_Table.pdf           # Complete Requirements Table deliverable[cite: 2]
├── use_case_diagram.pdf               # UML Use-Case Diagram[cite: 1, 2]
└── use_case_specification.pdf        # 1-Page Use-Case Flow document[cite: 1, 2]
