# API Conventions

## Overview

This document defines the conventions and standards for the UstaadX REST API.

## Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.ustaadx.com/api/v1
```

## Versioning

API versioning is done via URL path:
- `/api/v1/` - Version 1 (current)
- `/api/v2/` - Version 2 (future)

## HTTP Methods

| Method | Usage | Idempotent |
|--------|-------|------------|
| GET | Retrieve resources | Yes |
| POST | Create resources | No |
| PUT | Replace resources | Yes |
| PATCH | Update resources | No |
| DELETE | Delete resources | Yes |

## Request Format

### Headers

```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>
```

### Body

All request bodies must be valid JSON:

```json
{
  "field_name": "value",
  "nested_object": {
    "key": "value"
  },
  "array_field": [1, 2, 3]
}
```

## Response Format

### Success Response

```json
{
  "data": {
    "id": "123",
    "name": "Example",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### List Response

```json
{
  "data": [
    {"id": "1", "name": "Item 1"},
    {"id": "2", "name": "Item 2"}
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## Status Codes

### Success Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE with no response body |

### Client Error Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 400 | Bad Request | Invalid request format |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Error Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service error |
| 503 | Service Unavailable | Service temporarily down |

## Naming Conventions

### Endpoints

- Use **plural nouns** for resources: `/bookings`, `/providers`
- Use **kebab-case** for multi-word resources: `/service-categories`
- Use **nested routes** for relationships: `/bookings/123/reviews`

### Fields

- Use **snake_case** for field names: `created_at`, `user_id`
- Use **ISO 8601** for dates: `2024-01-15T10:30:00Z`
- Use **UUIDs** for IDs: `550e8400-e29b-41d4-a716-446655440000`

## Pagination

### Query Parameters

```
GET /api/v1/bookings?page=1&per_page=20
```

### Response

```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  },
  "links": {
    "first": "/api/v1/bookings?page=1&per_page=20",
    "last": "/api/v1/bookings?page=5&per_page=20",
    "prev": null,
    "next": "/api/v1/bookings?page=2&per_page=20"
  }
}
```

## Filtering

### Query Parameters

```
GET /api/v1/bookings?status=pending&service_type=plumber
```

### Multiple Values

```
GET /api/v1/bookings?status=pending,confirmed
```

## Sorting

### Query Parameters

```
GET /api/v1/bookings?sort=created_at        # Ascending
GET /api/v1/bookings?sort=-created_at       # Descending
GET /api/v1/bookings?sort=status,-created_at # Multiple
```

## Field Selection

### Sparse Fieldsets

```
GET /api/v1/bookings?fields=id,status,created_at
```

## Search

### Query Parameter

```
GET /api/v1/providers?q=plumber+karachi
```

## Authentication

### JWT Bearer Token

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Endpoints

```
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

## Rate Limiting

### Headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642248000
```

### Response (429)

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

## CORS

### Allowed Origins

Development:
- `http://localhost:3000`
- `http://localhost:8080`

Production:
- `https://app.ustaadx.com`
- `https://www.ustaadx.com`

### Headers

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## Example Endpoints

### Bookings

```
GET    /api/v1/bookings           # List bookings
POST   /api/v1/bookings           # Create booking
GET    /api/v1/bookings/:id       # Get booking
PUT    /api/v1/bookings/:id       # Update booking
DELETE /api/v1/bookings/:id       # Delete booking
PATCH  /api/v1/bookings/:id/status # Update status
```

### Providers

```
GET    /api/v1/providers          # List providers
POST   /api/v1/providers          # Create provider
GET    /api/v1/providers/:id      # Get provider
PUT    /api/v1/providers/:id      # Update provider
GET    /api/v1/providers/:id/reviews # Get reviews
```

### Authentication

```
POST   /api/v1/auth/register      # Register user
POST   /api/v1/auth/login         # Login
POST   /api/v1/auth/refresh       # Refresh token
POST   /api/v1/auth/logout        # Logout
GET    /api/v1/auth/me            # Get current user
```

## Request Examples

### Create Booking

```http
POST /api/v1/bookings
Content-Type: application/json
Authorization: Bearer <token>

{
  "service_type": "plumber",
  "description": "Fix leaking pipe",
  "location": {
    "address": "123 Main St, Karachi",
    "lat": 24.8607,
    "lng": 67.0011
  },
  "preferred_date": "2024-01-20",
  "preferred_time": "14:00:00"
}
```

### Response

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "service_type": "plumber",
    "description": "Fix leaking pipe",
    "status": "pending",
    "location": {
      "address": "123 Main St, Karachi",
      "lat": 24.8607,
      "lng": 67.0011
    },
    "preferred_date": "2024-01-20",
    "preferred_time": "14:00:00",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

## Error Handling

### Validation Error

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "invalid_format"
      },
      {
        "field": "phone",
        "message": "Phone number is required",
        "code": "required"
      }
    ]
  }
}
```

### Not Found Error

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": {
    "code": "NOT_FOUND",
    "message": "Booking not found",
    "resource": "booking",
    "id": "123"
  }
}
```

## WebSocket API

### Connection

```
ws://localhost:8000/ws/{user_id}?token=<jwt_token>
```

### Message Format

```json
{
  "type": "event",
  "event_type": "booking.updated",
  "data": {
    "booking_id": "123",
    "status": "confirmed"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Best Practices

1. **Use proper HTTP methods**: GET for reads, POST for creates, etc.
2. **Return appropriate status codes**: Match the response to the outcome
3. **Include timestamps**: Always use ISO 8601 format
4. **Use UUIDs for IDs**: More secure than sequential integers
5. **Validate input**: Return 422 with detailed errors
6. **Handle errors gracefully**: Provide helpful error messages
7. **Version your API**: Use URL versioning
8. **Document everything**: Keep API docs up to date
9. **Use pagination**: Don't return unbounded lists
10. **Implement rate limiting**: Protect against abuse

## Security

1. **Always use HTTPS** in production
2. **Validate all input** on the server
3. **Sanitize output** to prevent XSS
4. **Use parameterized queries** to prevent SQL injection
5. **Implement rate limiting** per user/IP
6. **Log security events** for audit trail
7. **Use secure headers** (HSTS, CSP, etc.)
8. **Rotate secrets regularly**

## Related Documentation

- [Architecture Overview](architecture.md)
- [Event System](event_system.md)
- [Setup Guide](setup_guide.md)
