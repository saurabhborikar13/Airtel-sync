# Project Udyam Digital: Data Privacy and Security Architecture Note
### Compliance with the Digital Personal Data Protection (DPDP) Act, 2023
**Prepared for:** Accel Telecom / Airtel Business · YTL Hackathon 2026 (Track A)  
**Author:** Project Udyam Digital Architecture Team  
**Date:** July 2026 / October 2026  

---

## 1. Executive Summary & Design Philosophy
Project Udyam Digital processes personal and enterprise identification data for India’s micro, small, and medium enterprise (MSME) owners. In strict adherence to the **Digital Personal Data Protection (DPDP) Act, 2023**, the platform is engineered under the principle of **Privacy by Design and Default (PbD)**. Every architectural layer—from conversational discovery to document verification and order dispatch—enforces data minimisation, purpose limitation, granular affirmative consent, dynamic PII masking, and cryptographic lifecycle management.

---

## 2. Core DPDP Act, 2023 Principles Implemented

### 2.1 Notice and Affirmative Consent (Section 5 & 6)
* **Granular Consent Modal:** Before any identifier or document is submitted, applicants are presented with a plain-language, unbundled consent modal available in English, Hindi (हिंदी), and regional languages (e.g., Tamil).
* **Clear Purpose Specification:** The notice specifies the exact statutory purpose: *"Verification of business identity for Department of Telecommunications (DOT) telecommunication subscriber onboarding and service provisioning."*
* **No Dark Patterns:** Checkboxes are unchecked by default; consent is never bundled with marketing or advertising permissions.
* **Withdrawal of Consent:** Applicants maintain the digital right to withdraw consent prior to service binding via self-service portal, triggering immediate token invalidation.

### 2.2 Purpose Limitation (Section 7)
* Data collected during the onboarding journey is strictly locked to subscriber identity verification and network provisioning.
* KYC dossiers (GSTIN, Udyam, ID proofs) are isolated in an encrypted tenant vault and are **never** shared with third-party advertising networks, cross-selling lead generators, or unauthorized external partners.

### 2.3 Data Minimisation & Collection Limitation (Section 6(1))
* **Only Statutory Essentials:** The platform collects only what is legally necessary to fulfill DOT/TRAI Know-Your-Customer mandates:
  1. Business registration identifier (GSTIN or Udyam number).
  2. Proof of principal place of business (Utility/Electricity bill dated within 90 days).
  3. Signatory Photo ID (Director/Partner/Proprietor authorization).
* Redundant or intrusive data (such as bank login credentials, social media handles, biometric data, or personal family records) is actively prohibited and blocked at the intake API.

### 2.4 Dynamic PII Masking in UI, Logs, and CRM (Section 8)
* **Zero Plaintext Identifiers:**
  * **GSTIN:** Masked dynamically across all interfaces and partner views (e.g., `37XXXXX5167L1ZS`).
  * **Udyam Number:** Masked as `UDYAM-XX-00-XXXXXXX`.
  * **Phone Numbers:** Masked as `+91 98XXXXXX25`.
* **Zero Logging of Sensitive Fields:** Application logs, telemetry streams, and crash analytics strictly scrub and hash all personal data before disk persistence. Field reps and channel partners can only view verification status badges (Approved/Pending), never raw identity numbers.

### 2.5 Storage Limitation & Automated Retention Schedule (Section 8(7))
* **Ephemeral Document Ingestion:** Raw uploaded image files (`.png`, `.jpg`, `.pdf`) are stored in an encrypted ephemeral landing cache.
* **Automated 30-Day Purge:** Once identity verification is successfully completed and approved by the telecom provisioning gateway, raw document images are scheduled for automated cryptographic erasure within **30 days**.
* **Immutable Audit Signatures:** Only SHA-256 cryptographic hashes of verified attributes and timestamped verification proofs are retained in the compliance ledger for statutory audit purposes.

### 2.6 Robust Technical & Security Safeguards (Section 8(5))
* **Encryption at Rest:** All applicant metadata and compliance logs are encrypted using **AES-256-GCM** with hardware security module (HSM) key management.
* **Encryption in Transit:** All client-server interactions, mock registry lookups, and webhook signals enforce **TLS 1.3** with strict HSTS headers.
* **Role-Based Access Control (RBAC):** Strict least-privilege principles dictate that local channel partners cannot inspect financial or personal identification documents submitted by the applicant.
* **AI Computer Vision Safeguards:** Client-side and server-side checks verify document integrity (detecting blur, skew, tampering, and checksum mismatches) before permanent ingestion, preventing fraudulent submission vectors.

---

## 3. Data Protection Officer (DPO) & Redressal Framework
In accordance with Section 8(9) of the DPDP Act, 2023:
* **Grievance Redressal:** Applicants can trigger data access, rectification, or deletion requests directly via the Self-Service Order Tracker.
* **SLA for Redressal:** All data subject queries and rectification requests are resolved within a mandatory 72-hour regulatory turnaround time.
* **Breach Notification Protocol:** In the unlikely event of any personal data compromise, automated webhook alerts immediately notify the Data Protection Board of India and affected data principals within 6 hours.
