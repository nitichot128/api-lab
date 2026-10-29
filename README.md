# API Testing Lab — ITDS362

API Testing lab using Python, pytest, and requests to test the QuickPizza API.

## Requirements

- Python 3.10 or newer
- Git
- Internet connection
- Windows PowerShell or another terminal

## Setup

1. Clone the repository:

   ```powershell
   git clone https://github.com/nitichot128/api-lab.git
   cd api-lab
   ```

2. Create and activate a virtual environment (Windows):

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Running Tests

Run all tests:

```powershell
pytest -v
```

Generate an HTML test report:

```powershell
pytest -v --html=report.html --self-contained-html
```

Open `report.html` in a browser to view the results.

## Test Results

- Passed: 32
- Expected Failures (XFAIL): 1
- Failed: 0
- Total: 33 test cases

The expected failure documents a known QuickPizza API defect involving the exclusion of all pizza cutting tools.

## Files

- `conftest.py` — Shared sessions and fixtures
- `test_*.py` — API test cases
- `RESULTS.md` — Lab results, defect report, and reflection
- `report.html` — HTML test report
- `requirements.txt` — Python dependencies

## Part A: Input Space Partitioning

### Input Domain Model — POST /api/ratings

The input domain model is based on four characteristics: the value of stars, the type of stars, pizza existence, and authentication token validity.

| Characteristic | Block | Test Input | Test Name |
|---|---|---|---|
| C1: Stars value | Below 1 | 0 | test_stars_out_of_range[0] |
| C1: Stars value | Valid 1–5 (Base) | 3 | test_base_choice_is_saved |
| C1: Stars value | Above 5 | 6 | test_stars_out_of_range[6] |
| C2: Stars type | Integer (Base) | 3 | test_base_choice_is_saved |
| C2: Stars type | Decimal | 3.5 | test_invalid_stars_type[decimal] |
| C2: Stars type | String | "3" | test_invalid_stars_type[string] |
| C2: Stars type | Missing | No stars field | test_invalid_stars_type[missing] |
| C3: Pizza | Exists (Base) | New pizza ID | test_base_choice_is_saved |
| C3: Pizza | Does not exist | 999999999 | test_nonexistent_pizza |
| C4: Token | Own token (Base) | Valid auth | test_base_choice_is_saved |
| C4: Token | None | No Authorization header | test_missing_token |
| C4: Token | Wrong length | token short | test_invalid_token_length |

### Base Choice Coverage

The base choice uses:
- Stars: 3
- Stars type: Integer
- Pizza: Existing pizza ID
- Token: Valid user token

Number of tests:

1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9 tests

All combinations coverage:

3 × 4 × 2 × 3 = 72 tests

Base choice coverage reduces the number of tests while covering every non-base block of each characteristic.