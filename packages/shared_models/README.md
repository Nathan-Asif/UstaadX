# Shared Models

This package contains data models shared between backend and mobile app.

## Purpose

- Define common data structures
- Ensure consistency across platforms
- Enable code reuse
- Facilitate API contract validation

## Future Structure

```
shared_models/
├── python/          # Python models (Pydantic)
│   ├── booking.py
│   ├── provider.py
│   └── user.py
├── dart/            # Dart models (Freezed)
│   ├── booking.dart
│   ├── provider.dart
│   └── user.dart
└── schemas/         # JSON schemas
    ├── booking.json
    ├── provider.json
    └── user.json
```

## Usage

### Python (Backend)

```python
from shared_models.python.booking import Booking

booking = Booking(
    id="123",
    service_type="plumber",
    status="pending"
)
```

### Dart (Mobile)

```dart
import 'package:shared_models/dart/booking.dart';

final booking = Booking(
  id: '123',
  serviceType: 'plumber',
  status: 'pending',
);
```

## Code Generation

Models should be generated from JSON schemas to ensure consistency.

Tools to consider:
- **quicktype**: Generate models from JSON schemas
- **OpenAPI Generator**: Generate from OpenAPI specs
- **Custom scripts**: Project-specific generation
