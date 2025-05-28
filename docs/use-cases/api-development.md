# Use Case: Building Robust APIs with Marvin

## 🌐 From Specification to Production API in Hours

Discover how Marvin transforms API development from a complex, error-prone process into a streamlined, AI-powered workflow that produces enterprise-grade APIs.

## The Traditional API Development Pain

Building APIs typically involves:
- ❌ Inconsistent endpoint design
- ❌ Missing error handling
- ❌ Poor documentation
- ❌ No input validation
- ❌ Security vulnerabilities
- ❌ Incomplete test coverage

## The Marvin API Advantage

With Marvin, you get:
- ✅ Consistent RESTful design
- ✅ Comprehensive error handling
- ✅ Auto-generated documentation
- ✅ Built-in validation & security
- ✅ Complete test suites
- ✅ Performance optimization

## 🏗️ Case Study: E-Commerce API

Let's build a complete e-commerce API to see Marvin in action.

### Step 1: Define Your API PRD

```markdown title="ecommerce-api-prd.md"
# E-Commerce API Specification

## Overview
RESTful API for a modern e-commerce platform supporting products, 
orders, payments, and inventory management.

## API Requirements

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Vendor, Customer)
- API key authentication for external integrations
- Rate limiting per user/IP

### Core Resources

#### Products
- CRUD operations for products
- Variant support (size, color, etc.)
- Image upload and management
- Category hierarchies
- Search and filtering
- Inventory tracking

#### Orders
- Order placement with cart validation
- Order status tracking
- Payment integration
- Shipping calculation
- Invoice generation
- Refund processing

#### Users
- Customer registration/profile
- Address management
- Order history
- Wishlist functionality
- Email notifications

### Technical Specifications
- RESTful design principles
- JSON request/response
- Pagination for list endpoints
- Sorting and filtering
- Webhook support for events
- API versioning (v1)

### Performance Requirements
- Response time < 200ms for reads
- Response time < 500ms for writes  
- Support 1000 requests/second
- 99.9% uptime SLA

### Security Requirements
- HTTPS only
- Input sanitization
- SQL injection prevention
- XSS protection
- CORS configuration
- Request signing for webhooks
```

### Step 2: Generate API Tasks with Marvin

```bash
marvin process ecommerce-api-prd.md --output ./api-tasks/
```

### Step 3: Marvin Creates Comprehensive API Tasks

#### Task: Product Endpoints Implementation

```xml
<?xml version="1.0" encoding="UTF-8"?>
<coding_task>
  <metadata>
    <task_id>api_products_001</task_id>
    <title>Product API Endpoints</title>
    <priority>high</priority>
    <estimated_effort>8 hours</estimated_effort>
  </metadata>
  
  <api_specification>
    <base_path>/api/v1/products</base_path>
    
    <endpoints>
      <endpoint>
        <method>GET</method>
        <path>/</path>
        <description>List all products with pagination</description>
        <query_parameters>
          <param name="page" type="integer" default="1">Page number</param>
          <param name="limit" type="integer" default="20" max="100">Items per page</param>
          <param name="sort" type="string" enum="price,name,created_at">Sort field</param>
          <param name="order" type="string" enum="asc,desc" default="asc">Sort order</param>
          <param name="category" type="string">Filter by category slug</param>
          <param name="min_price" type="number">Minimum price filter</param>
          <param name="max_price" type="number">Maximum price filter</param>
          <param name="in_stock" type="boolean">Filter in-stock only</param>
        </query_parameters>
        <response status="200">
          <schema>
            {
              "data": [
                {
                  "id": "uuid",
                  "name": "string",
                  "slug": "string",
                  "description": "string",
                  "price": "number",
                  "currency": "string",
                  "images": ["string"],
                  "category": {
                    "id": "uuid",
                    "name": "string",
                    "slug": "string"
                  },
                  "variants": [
                    {
                      "id": "uuid",
                      "name": "string",
                      "sku": "string",
                      "price": "number",
                      "stock": "integer",
                      "attributes": {}
                    }
                  ],
                  "stock": "integer",
                  "created_at": "datetime",
                  "updated_at": "datetime"
                }
              ],
              "meta": {
                "current_page": "integer",
                "total_pages": "integer",
                "total_items": "integer",
                "items_per_page": "integer"
              }
            }
          </schema>
        </response>
      </endpoint>
      
      <endpoint>
        <method>POST</method>
        <path>/</path>
        <description>Create a new product</description>
        <authentication>Bearer token (Admin, Vendor)</authentication>
        <request_body>
          <schema>
            {
              "name": "string (required, max: 200)",
              "description": "string (required)",
              "price": "number (required, min: 0)",
              "category_id": "uuid (required)",
              "images": ["string (url)"],
              "variants": [
                {
                  "name": "string",
                  "sku": "string (unique)",
                  "price": "number",
                  "stock": "integer (min: 0)",
                  "attributes": {
                    "size": "string",
                    "color": "string"
                  }
                }
              ],
              "meta_title": "string (max: 60)",
              "meta_description": "string (max: 160)",
              "tags": ["string"]
            }
          </schema>
          <validation_rules>
            <rule field="name">Required, unique per vendor</rule>
            <rule field="price">Must be positive number</rule>
            <rule field="sku">Unique across all products</rule>
            <rule field="images">Valid URLs, max 10 images</rule>
          </validation_rules>
        </request_body>
        <response status="201">Created product object</response>
        <errors>
          <error status="400">Validation errors</error>
          <error status="401">Unauthorized</error>
          <error status="403">Forbidden (not vendor/admin)</error>
          <error status="409">Duplicate SKU</error>
        </errors>
      </endpoint>
    </endpoints>
  </api_specification>
  
  <implementation_requirements>
    <requirement>Use Express.js with TypeScript</requirement>
    <requirement>Implement request validation middleware</requirement>
    <requirement>Add comprehensive error handling</requirement>
    <requirement>Include request/response logging</requirement>
    <requirement>Implement database transactions for creates/updates</requirement>
    <requirement>Add caching for GET requests (Redis)</requirement>
    <requirement>Include OpenAPI/Swagger documentation</requirement>
  </implementation_requirements>
  
  <security_measures>
    <measure>Input sanitization for all fields</measure>
    <measure>SQL injection prevention via parameterized queries</measure>
    <measure>Rate limiting: 100 requests/minute per IP</measure>
    <measure>File upload validation for images</measure>
    <measure>CORS configuration for allowed origins</measure>
  </security_measures>
  
  <testing_scenarios>
    <scenario>Valid product creation with all fields</scenario>
    <scenario>Product creation with missing required fields</scenario>
    <scenario>Duplicate SKU handling</scenario>
    <scenario>Pagination boundary testing</scenario>
    <scenario>Filter combination testing</scenario>
    <scenario>Authorization testing for different roles</scenario>
    <scenario>Rate limit enforcement</scenario>
    <scenario>Large payload handling</scenario>
  </testing_scenarios>
</coding_task>
```

### Step 4: AI Generates Production-Ready API Code

Feed this to your AI assistant and get:

```typescript
// Generated by AI from Marvin's structured task

import express, { Router } from 'express';
import { body, query, validationResult } from 'express-validator';
import { authenticate, authorize } from '../middleware/auth';
import { rateLimiter } from '../middleware/rateLimiter';
import { cache } from '../middleware/cache';
import { ProductService } from '../services/ProductService';
import { logger } from '../utils/logger';
import { ApiError } from '../utils/ApiError';

const router: Router = express.Router();
const productService = new ProductService();

// GET /api/v1/products - List products with pagination
router.get(
  '/',
  rateLimiter({ windowMs: 60000, max: 100 }),
  cache({ ttl: 300 }), // 5 minute cache
  [
    query('page').optional().isInt({ min: 1 }).toInt(),
    query('limit').optional().isInt({ min: 1, max: 100 }).toInt(),
    query('sort').optional().isIn(['price', 'name', 'created_at']),
    query('order').optional().isIn(['asc', 'desc']),
    query('category').optional().isString().trim(),
    query('min_price').optional().isFloat({ min: 0 }).toFloat(),
    query('max_price').optional().isFloat({ min: 0 }).toFloat(),
    query('in_stock').optional().isBoolean().toBoolean(),
  ],
  async (req, res, next) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        throw new ApiError(400, 'Validation failed', errors.array());
      }

      const filters = {
        page: req.query.page || 1,
        limit: req.query.limit || 20,
        sort: req.query.sort || 'created_at',
        order: req.query.order || 'asc',
        category: req.query.category,
        minPrice: req.query.min_price,
        maxPrice: req.query.max_price,
        inStock: req.query.in_stock,
      };

      logger.info('Fetching products', { filters, ip: req.ip });

      const result = await productService.getProducts(filters);

      res.json({
        data: result.products,
        meta: {
          current_page: result.currentPage,
          total_pages: result.totalPages,
          total_items: result.totalItems,
          items_per_page: result.itemsPerPage,
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

// POST /api/v1/products - Create new product
router.post(
  '/',
  authenticate,
  authorize(['admin', 'vendor']),
  rateLimiter({ windowMs: 60000, max: 20 }),
  [
    body('name').notEmpty().isLength({ max: 200 }).trim(),
    body('description').notEmpty().trim(),
    body('price').notEmpty().isFloat({ min: 0 }),
    body('category_id').notEmpty().isUUID(),
    body('images').optional().isArray({ max: 10 }),
    body('images.*').optional().isURL(),
    body('variants').optional().isArray(),
    body('variants.*.name').optional().isString().trim(),
    body('variants.*.sku').optional().isString().trim(),
    body('variants.*.price').optional().isFloat({ min: 0 }),
    body('variants.*.stock').optional().isInt({ min: 0 }),
    body('meta_title').optional().isLength({ max: 60 }).trim(),
    body('meta_description').optional().isLength({ max: 160 }).trim(),
    body('tags').optional().isArray(),
    body('tags.*').optional().isString().trim(),
  ],
  async (req, res, next) => {
    const transaction = await db.transaction();
    
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        throw new ApiError(400, 'Validation failed', errors.array());
      }

      // Check for duplicate SKUs
      if (req.body.variants) {
        for (const variant of req.body.variants) {
          if (variant.sku) {
            const existing = await productService.findBySku(variant.sku);
            if (existing) {
              throw new ApiError(409, `SKU already exists: ${variant.sku}`);
            }
          }
        }
      }

      const productData = {
        ...req.body,
        vendor_id: req.user.vendor_id || req.user.id,
        created_by: req.user.id,
      };

      logger.info('Creating product', { 
        name: productData.name, 
        vendor_id: productData.vendor_id 
      });

      const product = await productService.createProduct(productData, transaction);
      
      await transaction.commit();

      // Clear cache for product listings
      await cache.clear('products:*');

      res.status(201).json({
        data: product,
        message: 'Product created successfully',
      });
    } catch (error) {
      await transaction.rollback();
      next(error);
    }
  }
);

// Error handling middleware
router.use((error, req, res, next) => {
  logger.error('API Error', { error, path: req.path, method: req.method });
  
  const status = error.status || 500;
  const message = error.message || 'Internal server error';
  
  res.status(status).json({
    error: {
      status,
      message,
      details: error.details || undefined,
      timestamp: new Date().toISOString(),
      path: req.path,
    },
  });
});

export default router;

// Comprehensive test suite also generated
describe('Product API Endpoints', () => {
  describe('GET /api/v1/products', () => {
    it('should return paginated products', async () => {
      const response = await request(app)
        .get('/api/v1/products?page=1&limit=10')
        .expect(200);
      
      expect(response.body).toHaveProperty('data');
      expect(response.body).toHaveProperty('meta');
      expect(response.body.meta.items_per_page).toBe(10);
    });

    it('should filter by price range', async () => {
      const response = await request(app)
        .get('/api/v1/products?min_price=10&max_price=100')
        .expect(200);
      
      response.body.data.forEach(product => {
        expect(product.price).toBeGreaterThanOrEqual(10);
        expect(product.price).toBeLessThanOrEqual(100);
      });
    });

    it('should enforce rate limiting', async () => {
      // Make 101 requests
      for (let i = 0; i < 101; i++) {
        const response = await request(app).get('/api/v1/products');
        if (i === 100) {
          expect(response.status).toBe(429);
        }
      }
    });
  });

  describe('POST /api/v1/products', () => {
    it('should create product with valid data', async () => {
      const productData = {
        name: 'Test Product',
        description: 'Test description',
        price: 99.99,
        category_id: 'valid-uuid-here',
      };

      const response = await request(app)
        .post('/api/v1/products')
        .set('Authorization', 'Bearer valid-token')
        .send(productData)
        .expect(201);
      
      expect(response.body.data.name).toBe(productData.name);
    });

    it('should reject duplicate SKU', async () => {
      const productData = {
        name: 'Test Product',
        description: 'Test',
        price: 99.99,
        category_id: 'valid-uuid',
        variants: [{ sku: 'EXISTING-SKU', price: 99.99 }],
      };

      const response = await request(app)
        .post('/api/v1/products')
        .set('Authorization', 'Bearer valid-token')
        .send(productData)
        .expect(409);
      
      expect(response.body.error.message).toContain('SKU already exists');
    });
  });
});
```

## 📊 API Development Metrics

### Without Marvin
- **Design Time**: 2-3 days of meetings
- **Implementation**: 2-3 weeks
- **Documentation**: Often skipped
- **Testing**: Basic happy path only
- **Security**: Added as afterthought

### With Marvin
- **Design Time**: 1-2 hours (PRD writing)
- **Implementation**: 1-2 days
- **Documentation**: Auto-generated
- **Testing**: Comprehensive coverage
- **Security**: Built-in from start

## 🔐 Security Best Practices Enforced

Marvin ensures your API includes:

1. **Authentication & Authorization**
   ```typescript
   authenticate, // Verify JWT token
   authorize(['admin', 'vendor']), // Check roles
   ```

2. **Input Validation**
   ```typescript
   body('email').isEmail().normalizeEmail(),
   body('price').isFloat({ min: 0 }).toFloat(),
   ```

3. **Rate Limiting**
   ```typescript
   rateLimiter({ windowMs: 60000, max: 100 })
   ```

4. **SQL Injection Prevention**
   ```typescript
   // Parameterized queries enforced
   await db.query('SELECT * FROM products WHERE id = $1', [id]);
   ```

5. **Error Information Hiding**
   ```typescript
   // Production: Generic messages
   // Development: Detailed errors
   ```

## 🚀 Advanced API Patterns

### 1. GraphQL API Generation

```markdown title="graphql-api-prd.md"
# GraphQL API Specification

## Schema Requirements
- Type-safe schema definition
- Resolver implementation
- DataLoader for N+1 prevention
- Subscription support
- Schema stitching ready
```

### 2. Microservice APIs

```bash
# Generate coordinated microservice APIs
marvin process user-service-api.md --output ./services/user/
marvin process order-service-api.md --output ./services/order/
marvin process payment-service-api.md --output ./services/payment/
```

### 3. API Gateway Configuration

Marvin can generate:
- Route definitions
- Authentication middleware
- Rate limiting rules
- Request transformation
- Circuit breakers

## 📝 Documentation Generation

Marvin tasks include OpenAPI specs:

```yaml
# Auto-generated swagger.yaml
openapi: 3.0.0
info:
  title: E-Commerce API
  version: 1.0.0
paths:
  /api/v1/products:
    get:
      summary: List products
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
      responses:
        200:
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductList'
```

## 🧪 Comprehensive Testing

Every API task includes:

1. **Unit Tests**: Service layer testing
2. **Integration Tests**: Full request/response
3. **Load Tests**: Performance validation
4. **Security Tests**: Penetration testing
5. **Contract Tests**: API compatibility

## 💡 Pro Tips for API Development

### DO's:
- ✅ Include example requests/responses in PRD
- ✅ Specify error scenarios explicitly
- ✅ Define rate limits per endpoint
- ✅ Include webhook specifications
- ✅ Plan API versioning strategy

### DON'Ts:
- ❌ Skip authentication requirements
- ❌ Ignore pagination for list endpoints
- ❌ Forget about CORS configuration
- ❌ Omit validation rules
- ❌ Skip performance requirements

## 🎯 Real-World Success

**FinTech Startup** built their entire API with Marvin:

> "We launched a secure, compliant financial API in 3 weeks instead of 3 months. Marvin's structured approach meant every endpoint had proper validation, error handling, and documentation from day one."

### Results:
- 0 security vulnerabilities in pen testing
- 100% API documentation coverage
- 99.99% uptime in first year
- 50ms average response time
- SOC2 compliance achieved faster

## 📚 Resources

- [API Design Best Practices](../guides/api-design.md)
- [Security Checklist](../guides/api-security.md)
- [Performance Optimization](../guides/api-performance.md)
- [API Testing Guide](../guides/api-testing.md)

---

**Ready to build bulletproof APIs?** Let Marvin transform your API specifications into production-ready code →