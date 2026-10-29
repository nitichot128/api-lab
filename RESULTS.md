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
| Read (GET) | 404 Not Found | Yes |
| Update (PUT) | 400 Bad Request | Yes |
| Delete (DELETE) | 400 Bad Request | Yes |

## Part B — Reflection

### 1. API tests vs unit tests with stubs
**Question:** Name two kinds of failure that real-server API tests can find but unit tests with stubs cannot. Give one reason to write unit tests with stubs as well.

**Answer:** API Testing สามารถตรวจพบปัญหาการเชื่อมต่อระหว่างระบบ และปัญหาที่เกิดจาก Server หรือ Database จริง ซึ่ง Unit Test แบบ Stub อาจตรวจไม่พบ ส่วน Unit Test ยังจำเป็นเพราะทำงานเร็วและช่วยตรวจสอบแต่ละฟังก์ชันได้ง่าย

### 2. Fresh users and shared test data
**Question:** Why does every test create its own user with a new name instead of using the public token? How will you apply the same idea to the shared shop or hotel in Project 2?

**Answer:** เพื่อให้แต่ละ Test เป็นอิสระ ไม่รบกวนข้อมูลของคนอื่น และไม่เกิดปัญหาจากการใช้ข้อมูลร่วมกัน สำหรับ Project 2 จะสร้างข้อมูลทดสอบของกลุ่มเองและลบข้อมูลหลังทดสอบ

### 3. Shared session
**Question:** Why do the tests send every request through one session? If you did Step 0.12, describe the three runs.

**Answer:** เพราะ QuickPizza มีหลาย Server การใช้ Session ช่วยเก็บ Cookie เพื่อให้ Request ไปยัง Server เดิม โดยทดลองไม่ใช้ Session ทั้ง 3 ครั้ง พบว่า Login ล้มเหลวด้วย HTTP 401 ทุกครั้ง

### 4. Excluded-tools defect
**Question:** Which excluded-tools block revealed the defect? Why is HTTP 500 with an empty body worse than HTTP 400 with a message? Why keep the test as `xfail`?

**Answer:** พบ Bug เมื่อ Exclude เครื่องมือทั้ง 3 ชนิด ทำให้ API ตอบ HTTP 500 และไม่มี Response Body แทนที่จะตอบ HTTP 400 พร้อมข้อความ Error ซึ่งทำให้ Client จัดการข้อผิดพลาดได้ยาก จึงใช้ xfail เพื่อเก็บ Test นี้ไว้ตรวจสอบจนกว่าจะแก้ Bug

### 5. Coverage calculations
**Question:** How many tests does base choice coverage need for the Step A1 model, and how many would all combinations coverage need? Show your calculation.

- Base choice coverage: 1 + 2 + 3 + 1 + 2 = 9 Tests
- All combinations coverage: 3 × 4 × 2 × 3 = 72 Tests

### 6. Authorization status codes
**Question:** In Step A4, what status codes did another user receive when reading, updating, and deleting a rating? Which codes would you expect? Is the difference a defect? Explain.

**Answer:** ผลการทดสอบพบว่า GET ได้ 404, PUT ได้ 400 และ DELETE ได้ 400

GET 404 ถือว่าเหมาะสมเพราะช่วยซ่อนข้อมูล ส่วน PUT และ DELETE ควรตอบ 403 Forbidden มากกว่า 400 Bad Request จึงอาจเป็นข้อบกพร่องด้านการเลือก HTTP Status Code แต่ระบบยังป้องกันการเข้าถึงข้อมูลของผู้อื่นได้

### 7. Made-up token experiment
**Question:** Create `madeup.txt` containing `Authorization: token 0000000000000000` and run `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings`. What comes back? Is it a defect? What could a stranger do with it on a real system?

- Actual response/status: 200
- Analysis / security implications: {"ratings":[{"id":1,"stars":5,"pizza_id":1},{"id":2,"stars":1,"pizza_id":2},{"id":3,"stars":1,"pizza_id":3},{"id":4,"stars":5,"pizza_id":9},{"id":5,"stars":5,"pizza_id":11},{"id":6,"stars":5,"pizza_id":14},{"id":7,"stars":5,"pizza_id":22},{"id":8,"stars":5,"pizza_id":24},{"id":11,"stars":5,"pizza_id":25},{"id":12,"stars":5,"pizza_id":1},{"id":15,"stars":5,"pizza_id":32},{"id":16,"stars":5,"pizza_id":34},{"id":18,"stars":5,"pizza_id":44},{"id":19,"stars":2,"pizza_id":1},{"id":20,"stars":5,"pizza_id":52},{"id":23,"stars":5,"pizza_id":63},{"id":24,"stars":5,"pizza_id":81},{"id":27,"stars":5,"pizza_id":89},{"id":28,"stars":5,"pizza_id":98},{"id":31,"stars":5,"pizza_id":102},{"id":32,"stars":5,"pizza_id":104},{"id":33,"stars":5,"pizza_id":106},{"id":34,"stars":2,"pizza_id":1},{"id":35,"stars":5,"pizza_id":116},{"id":36,"stars":5,"pizza_id":117},{"id":56,"stars":5,"pizza_id":190},{"id":59,"stars":1,"pizza_id":198},{"id":60,"stars":4,"pizza_id":198},{"id":61,"stars":4,"pizza_id":200},{"id":62,"stars":5,"pizza_id":200},{"id":63,"stars":5,"pizza_id":201},{"id":68,"stars":5,"pizza_id":229},{"id":69,"stars":5,"pizza_id":233},{"id":71,"stars":5,"pizza_id":259},{"id":75,"stars":5,"pizza_id":283},{"id":77,"stars":2,"pizza_id":1},{"id":92,"stars":5,"pizza_id":342},{"id":93,"stars":5,"pizza_id":345},{"id":94,"stars":5,"pizza_id":352},{"id":95,"stars":5,"pizza_id":353},{"id":96,"stars":5,"pizza_id":356},{"id":97,"stars":5,"pizza_id":369},{"id":98,"stars":5,"pizza_id":372},{"id":101,"stars":2,"pizza_id":1},{"id":102,"stars":5,"pizza_id":379},{"id":103,"stars":5,"pizza_id":386},{"id":104,"stars":5,"pizza_id":395},{"id":105,"stars":2,"pizza_id":1},{"id":109,"stars":5,"pizza_id":422},{"id":111,"stars":5,"pizza_id":439}]}

### 8. API tests vs web-page tests
**Question:** Name one thing that an API test checks better than a test through web pages, and one thing that only a web-page test can check.

**Answer:** API Testing เหมาะกับการตรวจสอบ Status Code, JSON Response และการจัดการ Error ส่วน Web UI Testing เหมาะกับการตรวจสอบหน้าตาเว็บไซต์ ปุ่ม และการแสดงผลที่ผู้ใช้มองเห็น

---

## Final test run (optional record)

- Command: `pytest -v --html=report.html --self-contained-html`
- Passed: [กรอก]
- Failed: [กรอก]
- Xfailed: [กรอก]
- Report file: `report.html`
- Date tested: [กรอกวันที่]
