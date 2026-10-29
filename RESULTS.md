# API lab results

> ITDS362 — API Testing with pytest and requests
> ชื่อ-นามสกุล: นิธิโชติ ไชยสิทธิ์
> รหัสนักศึกษา: 6787048
> GitHub Repository: https://github.com/nitichot128/api-lab

## Part 0

### Step 0.1 — Pizza names
- Number of pizza names: **18**

### Step 0.3 — Request without a token
- HTTP status code: **401**

### Step 0.4 — Vegetarian pizza
- Pizza name returned by the API: **The Soft Margherita**

### Step 0.12 — Without a session (optional)

| Run | Result (Passed/Failed) | HTTP status / error (if any) |
|---|---|---|
| 1 | FAILED | 401 Unauthorized |
| 2 | FAILED | 401 Unauthorized |
| 3 | FAILED | 401 Unauthorized |

### Step 0.16 — Excluded tools partitions
Characteristic: **How many of the three tools are excluded?**

| Block | Example `excludedTools` | Test result / HTTP status |
|---|---|---|
| 0 excluded | `[]` | Pass/200 |
| 1 excluded | `["Knife"]` | Pass/200 |
| 2 excluded | `["Knife", "Scissors"]` | Pass/200 |
| 3 excluded | `["Knife", "Pizza cutter", "Scissors"]` | Failed/500 |

- Block that revealed the defect: **3**
- curl verification command: `curl.exe -i -H "@auth.txt" -H "Content-Type: application/json" --data-binary "@excluded.json" https://quickpizza.grafana.com/api/pizza`
- body file used: `{"excludedTools": ["Knife","Pizza cutter","Scissors"]}`

## Defect report

- **Title:** HTTP 500 Internal Server Error when all pizza cutting tools are excluded.
- **Request:**
    Method: POST
    URL: https://quickpizza.grafana.com/api/pizza
    Headers:
        Authorization: token abcdef0123456789
        Content-Type: application/json
    JSON Body:
    {
        "excludedTools": [
            "Knife",
            "Pizza cutter",
            "Scissors"
        ]
    }
- **Expected result:** HTTP 400 Bad Request with a JSON error message explaining that no pizza can satisfy the request.
- **Actual result:** HTTP 500 Internal Server Error with an empty response body (Content-Length: 0). The API did not return a JSON error message.
- **Severity:** Medium — The API does not handle a request that excludes all available cutting tools correctly. Instead of returning a clear client error, it returns an internal server error without an explanation, making it difficult for clients to handle the failure.

## Part A

### Step A4 — Rating ownership authorization

| Attempt by another user | Actual HTTP status | Rating unchanged when checked by owner? |
|---|---|---|
| Read (GET) | [กรอก] | [กรอก] |
| Update (PUT) | [กรอก] | [กรอก] |
| Delete (DELETE) | [กรอก] | [กรอก] |

## Part B — Reflection

### 1. API tests vs unit tests with stubs
**Question:** Name two kinds of failure that real-server API tests can find but unit tests with stubs cannot. Give one reason to write unit tests with stubs as well.

**Answer:** [กรอกคำตอบ]

### 2. Fresh users and shared test data
**Question:** Why does every test create its own user with a new name instead of using the public token? How will you apply the same idea to the shared shop or hotel in Project 2?

**Answer:** [กรอกคำตอบ]

### 3. Shared session
**Question:** Why do the tests send every request through one session? If you did Step 0.12, describe the three runs.

**Answer:** [กรอกคำตอบ]

### 4. Excluded-tools defect
**Question:** Which excluded-tools block revealed the defect? Why is HTTP 500 with an empty body worse than HTTP 400 with a message? Why keep the test as `xfail`?

**Answer:** [กรอกคำตอบ]

### 5. Coverage calculations
**Question:** How many tests does base choice coverage need for the Step A1 model, and how many would all combinations coverage need? Show your calculation.

- Base choice coverage: [แสดงวิธีคิด]
- All combinations coverage: [แสดงวิธีคิด]

### 6. Authorization status codes
**Question:** In Step A4, what status codes did another user receive when reading, updating, and deleting a rating? Which codes would you expect? Is the difference a defect? Explain.

**Answer:** [กรอกคำตอบโดยอ้างอิงผลจริง]

### 7. Made-up token experiment
**Question:** Create `madeup.txt` containing `Authorization: token 0000000000000000` and run `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings`. What comes back? Is it a defect? What could a stranger do with it on a real system? **Only read with this token; do not create or change data.**

- Actual response/status: [กรอก]
- Analysis / security implications: [กรอก]

### 8. API tests vs web-page tests
**Question:** Name one thing that an API test checks better than a test through web pages, and one thing that only a web-page test can check.

**Answer:** [กรอกคำตอบ]

---

## Final test run (optional record)

- Command: `pytest -v --html=report.html --self-contained-html`
- Passed: [กรอก]
- Failed: [กรอก]
- Xfailed: [กรอก]
- Report file: `report.html`
- Date tested: [กรอกวันที่]
