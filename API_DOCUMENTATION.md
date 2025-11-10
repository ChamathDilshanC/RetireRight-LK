# 🚀 RetireRight LK - API Documentation

**Base URL:** `https://coral-app-oev86.ondigitalocean.app`

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Calculator Endpoints](#calculator-endpoints)
3. [User Profile](#user-profile)
4. [Calculation History](#calculation-history)
5. [Postman Collection](#postman-collection)

---

## 🔐 Authentication

All authenticated endpoints require a Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase-id-token>
```

---

## 📡 API Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**

```json
{
  "status": "healthy",
  "service": "RetireRight LK API"
}
```

**Example:**

```bash
curl https://coral-app-oev86.ondigitalocean.app/health
```

---

## 🔐 Authentication Endpoints

### 1.1 Verify Firebase Token

**POST** `/api/auth/verify`

Verify Firebase token and create/update user in database.

**Request Body:**

```json
{
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
}
```

**Response:**

```json
{
  "success": true,
  "user": {
    "id": 1,
    "uid": "firebase-uid-123",
    "email": "user@example.com",
    "name": "John Doe",
    "profilePicture": "https://...",
    "emailVerified": true,
    "createdAt": "2025-11-10T10:00:00",
    "lastLogin": "2025-11-10T12:00:00"
  }
}
```

**cURL:**

```bash
curl -X POST https://coral-app-oev86.ondigitalocean.app/api/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"idToken":"YOUR_FIREBASE_TOKEN"}'
```

---

### 1.2 Get Current User

**GET** `/api/auth/me`

Get current authenticated user information.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Response:**

```json
{
  "success": true,
  "user": {
    "id": 1,
    "uid": "firebase-uid-123",
    "email": "user@example.com",
    "name": "John Doe",
    "profilePicture": "https://...",
    "emailVerified": true,
    "createdAt": "2025-11-10T10:00:00"
  }
}
```

**cURL:**

```bash
curl https://coral-app-oev86.ondigitalocean.app/api/auth/me \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

---

### 1.3 Logout

**POST** `/api/auth/logout`

Logout current user (clears session).

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Response:**

```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 1.4 Delete Account

**DELETE** `/api/auth/delete`

Permanently delete user account and all associated data.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Response:**

```json
{
  "success": true,
  "message": "Account deleted successfully"
}
```

---

## 🧮 Calculator Endpoints

### 2.1 Calculate Monthly Contributions

**POST** `/api/calculator/contributions`

Calculate monthly EPF/ETF contributions based on salary.

**Request Body:**

```json
{
  "basicSalary": 75000,
  "employeeEpfRate": 10
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "basicSalary": 75000,
    "employeeContribution": 7500,
    "employerEpfContribution": 9000,
    "employerEtfContribution": 2250,
    "totalEpf": 16500,
    "totalEtf": 2250,
    "totalContributions": 18750
  }
}
```

**cURL:**

```bash
curl -X POST https://coral-app-oev86.ondigitalocean.app/api/calculator/contributions \
  -H "Content-Type: application/json" \
  -d '{
    "basicSalary": 75000,
    "employeeEpfRate": 10
  }'
```

---

### 2.2 Retirement Projection

**POST** `/api/calculator/retirement-projection`

Calculate complete retirement savings projection with yearly breakdown.

**Request Body:**

```json
{
  "currentAge": 28,
  "retirementAge": 60,
  "basicSalary": 75000,
  "employeeEpfRate": 10,
  "annualIncrement": 5,
  "epfInterestRate": 9.5,
  "currentEpfBalance": 500000,
  "inflationRate": 6
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "finalBalance": 12500000,
    "yearlyBreakdown": [
      {
        "year": 2025,
        "age": 28,
        "salary": 75000,
        "totalContributions": 225000,
        "interest": 47500,
        "closingBalance": 772500
      },
      ...
    ],
    "purchasingPower": {
      "finalBalance": 12500000,
      "inflationRate": 6,
      "years": 32,
      "todayValue": 2100000
    },
    "monthlyPensionOptions": {
      "twentyYears": 95000,
      "twentyFiveYears": 88000
    }
  }
}
```

**cURL:**

```bash
curl -X POST https://coral-app-oev86.ondigitalocean.app/api/calculator/retirement-projection \
  -H "Content-Type: application/json" \
  -d '{
    "currentAge": 28,
    "retirementAge": 60,
    "basicSalary": 75000,
    "employeeEpfRate": 10,
    "annualIncrement": 5,
    "epfInterestRate": 9.5,
    "currentEpfBalance": 500000,
    "inflationRate": 6
  }'
```

---

### 2.3 Compare Scenarios

**POST** `/api/calculator/scenarios/compare`

Compare multiple retirement scenarios side by side.

**Request Body:**

```json
{
  "scenarios": [
    {
      "name": "Conservative",
      "currentAge": 28,
      "retirementAge": 60,
      "basicSalary": 75000,
      "employeeEpfRate": 8,
      "annualIncrement": 3,
      "epfInterestRate": 9.5
    },
    {
      "name": "Aggressive",
      "currentAge": 28,
      "retirementAge": 60,
      "basicSalary": 75000,
      "employeeEpfRate": 10,
      "annualIncrement": 7,
      "epfInterestRate": 9.5
    }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "scenarios": [
      {
        "name": "Conservative",
        "finalBalance": 10500000,
        "totalContributions": 6200000,
        "totalInterest": 4300000
      },
      {
        "name": "Aggressive",
        "finalBalance": 15200000,
        "totalContributions": 8500000,
        "totalInterest": 6700000
      }
    ]
  }
}
```

---

## 👤 User Profile Endpoints

### 3.1 Get User Profile

**GET** `/api/user/profile`

Get user profile and salary information.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Response:**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "profilePicture": "https://..."
    },
    "salaryProfile": {
      "id": 1,
      "currentBasicSalary": 75000,
      "age": 28,
      "yearsOfService": 5,
      "retirementAge": 60,
      "epfRate": 10,
      "expectedSalaryIncrement": 5,
      "currentEpfBalance": 500000,
      "createdAt": "2025-11-10T10:00:00",
      "updatedAt": "2025-11-10T12:00:00"
    }
  }
}
```

**cURL:**

```bash
curl https://coral-app-oev86.ondigitalocean.app/api/user/profile \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

---

### 3.2 Update User Profile

**PUT** `/api/user/profile`

Update or create user salary profile.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Request Body:**

```json
{
  "currentBasicSalary": 80000,
  "age": 29,
  "yearsOfService": 6,
  "retirementAge": 60,
  "epfRate": 10,
  "expectedSalaryIncrement": 5,
  "currentEpfBalance": 600000
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "currentBasicSalary": 80000,
    "age": 29,
    "yearsOfService": 6,
    "retirementAge": 60,
    "epfRate": 10,
    "expectedSalaryIncrement": 5,
    "currentEpfBalance": 600000,
    "updatedAt": "2025-11-10T13:00:00"
  }
}
```

---

## 📊 Calculation History Endpoints

### 4.1 Get Calculation History

**GET** `/api/user/calculations`

Get user's saved calculation history.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Query Parameters:**

- `limit` (optional): Number of records to return (default: 10)
- `offset` (optional): Number of records to skip (default: 0)

**Response:**

```json
{
  "success": true,
  "data": {
    "calculations": [
      {
        "id": 1,
        "calculationType": "retirement_projection",
        "inputData": {
          "currentAge": 28,
          "retirementAge": 60,
          "basicSalary": 75000
        },
        "result": {
          "finalBalance": 12500000
        },
        "createdAt": "2025-11-10T10:00:00"
      }
    ],
    "total": 15,
    "limit": 10,
    "offset": 0
  }
}
```

**cURL:**

```bash
curl "https://coral-app-oev86.ondigitalocean.app/api/user/calculations?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

---

### 4.2 Save Calculation

**POST** `/api/user/calculations`

Save a calculation to history.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Request Body:**

```json
{
  "calculationType": "retirement_projection",
  "inputData": {
    "currentAge": 28,
    "retirementAge": 60,
    "basicSalary": 75000
  },
  "result": {
    "finalBalance": 12500000
  }
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "calculationType": "retirement_projection",
    "createdAt": "2025-11-10T14:00:00"
  }
}
```

---

### 4.3 Delete Calculation

**DELETE** `/api/user/calculations/<id>`

Delete a specific calculation from history.

**Headers:**

```
Authorization: Bearer <firebase-token>
```

**Response:**

```json
{
  "success": true,
  "message": "Calculation deleted successfully"
}
```

---

## 🚨 Error Responses

All endpoints may return these error formats:

### 400 Bad Request

```json
{
  "error": "Missing required field",
  "message": "basicSalary is required"
}
```

### 401 Unauthorized

```json
{
  "error": "Invalid token",
  "message": "Failed to verify token"
}
```

### 404 Not Found

```json
{
  "error": "Not found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Calculation failed",
  "message": "Internal server error"
}
```

---

## 📦 Postman Collection

Import this JSON into Postman to test all endpoints:

### Quick Import URL:

```
https://coral-app-oev86.ondigitalocean.app/health
```

See `POSTMAN_COLLECTION.json` file in this repository for the complete collection.

---

## 🔑 Environment Variables for Postman

Create these variables in your Postman environment:

| Variable         | Value                                        |
| ---------------- | -------------------------------------------- |
| `base_url`       | `https://coral-app-oev86.ondigitalocean.app` |
| `firebase_token` | Your Firebase ID token                       |

---

## 📝 Notes

- All dates are in ISO 8601 format
- All monetary values are in LKR (Sri Lankan Rupees)
- Interest rates and percentages are in decimal format (e.g., 9.5 = 9.5%)
- Firebase tokens expire after 1 hour - refresh as needed

---

## 🛠️ Testing with cURL

### Example: Complete Workflow

1. **Check Health:**

```bash
curl https://coral-app-oev86.ondigitalocean.app/health
```

2. **Calculate Contributions:**

```bash
curl -X POST https://coral-app-oev86.ondigitalocean.app/api/calculator/contributions \
  -H "Content-Type: application/json" \
  -d '{"basicSalary": 75000, "employeeEpfRate": 10}'
```

3. **Get Retirement Projection:**

```bash
curl -X POST https://coral-app-oev86.ondigitalocean.app/api/calculator/retirement-projection \
  -H "Content-Type: application/json" \
  -d '{
    "currentAge": 28,
    "retirementAge": 60,
    "basicSalary": 75000,
    "employeeEpfRate": 10,
    "annualIncrement": 5,
    "epfInterestRate": 9.5,
    "currentEpfBalance": 500000
  }'
```

---

## 📞 Support

For issues or questions:

- Check logs in DigitalOcean Dashboard
- Verify Firebase token is valid
- Ensure all required fields are provided

---

**Last Updated:** November 10, 2025
**API Version:** 1.0.0
**Base URL:** https://coral-app-oev86.ondigitalocean.app
