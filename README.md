# [drift_cult](https://drift-cult-9f60af6d7463.herokuapp.com) (https://driftcult.art)

Developer: Max Kaening ([Maxcode0101](https://www.github.com/Maxcode0101))

[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Maxcode0101/drift_cult)](https://www.github.com/Maxcode0101/drift_cult/commits/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/Maxcode0101/drift_cult)](https://www.github.com/Maxcode0101/drift_cult/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/Maxcode0101/drift_cult)](https://www.github.com/Maxcode0101/drift_cult)

---

**Drift Cult** is a modern, full-stack e-commerce web application built using Django, PostgreSQL, and Stripe. It serves as the online storefront for a countercultural surf, skate, and outdoor clothing brand that emphasizes durability, authenticity, and non-mainstream values.

The application is designed for a niche community of independent, style-conscious individuals who reject fast fashion in favor of minimalist design and long-lasting quality. The platform provides a streamlined shopping experience, allowing users to browse curated products, manage their cart, and complete secure purchases.

From a technical perspective, Drift Cult incorporates user authentication via Allauth, dynamic product filtering, Stripe-powered payment flows, responsive UI with Bootstrap 4, automated confirmation emails, and an admin interface for managing inventory and orders. Media files are hosted via AWS S3, and the application is deployed on Heroku with PostgreSQL as the production database.

Drift Cult reflects both a technical implementation of best practices and a brand-driven digital experience that connects directly with its target audience.

![screenshot](documentation/mockup.png)

source: [drift_cult amiresponsive](https://ui.dev/amiresponsive?url=https://driftcult.art)


---


## UX

### The 5 Planes of UX

#### 1. Strategy

**Purpose**
- Deliver a performant and intuitive e-commerce experience for Drift Cult, a minimalist surf, skate, and outdoor apparel brand.
- Empower authenticated users with streamlined checkout and profile functionality.
- Enable staff to manage orders and inventory via a secure internal dashboard.

**Primary User Needs**
- Guest users need to browse products and sign up to the newsletter without registration.
- Authenticated users require fast access to their profile, order history, and payment confirmations.
- Site admins must be able to create, edit, delete, and track products and orders with minimal friction.

**Business Goals**
- Build a sustainable brand platform rooted in counter-mainstream values and raw authenticity.
- Support growth of a global underground audience of surfers, skaters, and creatives.
- Facilitate conversions through a fast, mobile-first UI with secure Stripe integration and automated email flows.

#### 2. Scope

**Features**
- Full shopping flow: browse, search, filter, product detail view, cart management, and checkout.
- User account system: sign up, login, order history, and email confirmations.
- Admin dashboard: product and order CRUD operations, inventory sizing, and email triggers on status updates.
- Newsletter modal and footer signup, with AJAX handling and confirmation logic.
- Legal pages: FAQ, Terms, Refund Policy, Contact Form.
- SEO implementation: sitemap, robots.txt, meta tags.

**Content Requirements**
- Product data: name, price, category, description, image, and sizes.
- Legal disclaimers: terms, return policy, community-first philosophy.
- Minimalist layout: brand story, community section, and high-contrast visual hierarchy.

#### 3. Structure

**Information Architecture**
- **Navbar Navigation**:
  - Home, Shop, Cart, Community, About, Contact, Profile (if logged in)
- **Footer Navigation**:
  - Instagram, TikTok, Facebook, Twitter, Contact, FAQ, Terms, Refund Policy

**User Flow**
1. User lands on homepage with brand intro and logo hero section.
2. User browses or filters products via `/shop/`, views detail page, selects size.
3. Adds items to cart, updates quantities, and proceeds to checkout (Stripe).
4. On success, confirmation email is triggered and order stored.
5. Admin can log in and access a dashboard via /store/admin-dashboard/ to manage inventory and orders.

#### 4. Skeleton

**Wireframes**

To guide the design and layout of the Drift Cult e-commerce platform, both ASCII-style structural diagrams and high-fidelity wireframes were developed. These provide a clear visual reference for the UX structure across all devices and user flows.

The following pages were wireframed to cover core user interactions from browsing and shopping to checkout and admin management:

| Page | ASCII Wireframe | High-Fidelity Wireframe |
| --- | --- | --- |
| Home | ![Home ASCII](documentation/home.png) | ![Home](documentation/home_page.png) |
| Shop / Product List | ![Shop ASCII](documentation/shop_ascii.png) | ![Shop](documentation/products_page.png) |
| Product Detail | ![Product Detail ASCII](documentation/product_detail_ascii.png) | ![Product Detail](documentation/product_detail_page.png) |
| Cart & Checkout | ![Cart & Checkout ASCII](documentation/cart_and_checkout_ascii.png) | ![Cart](documentation/cart_page.png), ![Checkout](documentation/checkout_page.png) |
| Login / Signup | ![Login ASCII](documentation/login_signup_ascii.png) | ![Login](documentation/login_sign_up_page.png) |
| Admin Dashboard | ![Admin ASCII](documentation/admin_dashboard_ascii.png) | ![Admin](documentation/admin_dashboard.png) |

- These wireframes reflect a clean, mobile-first layout optimized for usability, discoverability, and Drift Cult’s brand tone.
- Visual consistency through Bootstrap 4 utility classes.
- AJAX used for newsletter UX without full page reloads.

#### 5. Surface

**Visual Design**
- Brand colors: monochrome palette with clean accents for CTAs and alerts.
- Typography: Montserrat for headers and Lato for body text.
- Imagery: high-resolution product shots hosted on AWS S3; transparent brand logo featured on homepage.
- Layout: minimalist, responsive, built with Bootstrap 4 grid and media queries.


## User Stories

| Target | Expectation | Outcome |
| --- | --- | --- |
| As a customer | I want to browse and search for products | so that I can find the items I want to purchase easily. |
| As a customer | I want to create an account | so that I can save my order history and checkout faster. |
| As a customer | I want to add products to a shopping cart | so that I can purchase them later. |
| As a customer | I want to update product quantities in my cart | so that I can adjust my order before checkout. |
| As a customer | I want to securely pay for my order with Stripe | so that I can receive my items. |
| As a customer | I want to receive confirmation messages and emails after checkout | so that I know my order was successful. |
| As a customer | I want to see my order history | so that I can track my purchases. |
| As an admin | I want to manage products and orders | so that I can keep the store updated. |
| As a business owner | I want my store to rank higher on search engines | so that more customers can find it. |
| As a customer | I want the website to work smoothly on mobile | so that I can shop from any device. |


## Features

### Existing Features

| Feature | Notes | Screenshot |
| --- | --- | --- |
| Register | Users can create an account with email and password. Email confirmation is required. | ![screenshot](documentation/readme/features/register.png) |
| Login | Existing users can securely log in. | ![screenshot](documentation/readme/features/login.png) |
| Logout | Users can log out of their account from the navigation menu. | ![screenshot](documentation/readme/features/logout.png) |
| Product List | Users can browse all available products with search and category filtering. | ![screenshot](documentation/readme/features/product-list.png) |
| Product Details | Shows product description, image, price, and size options. | ![screenshot](documentation/readme/features/product-details.png) |
| Add to Cart | Adds a product to the shopping cart with selected size. | ![screenshot](documentation/readme/features/add-to-bag.png) |
| Remove from Cart | Users can remove items from the shopping cart. | ![screenshot](documentation/readme/features/remove-from-bag.png) |
| Checkout | Checkout with Stripe integration and email input. | ![screenshot](documentation/readme/features/checkout.png) |
| Order Confirmation | Confirmation screen displayed after a successful purchase. | ![screenshot](documentation/readme/features/order-confirmation.png) |
| Order History | Logged-in users can view past orders. | ![screenshot](documentation/readme/features/order-history.png) |
| Order Management (Admin) | Admin dashboard to update or delete customer orders. | ![screenshot](documentation/readme/features/order-management.png) |
| Product Management (Admin) | Add, edit, or delete products via the admin interface. | ![screenshot](documentation/readme/features/product-management.png) |
| Newsletter Modal | AJAX-based modal for newsletter signup on homepage. | ![screenshot](documentation/readme/features/modal.png) |
| Contact Form | Users can send a message via a contact form. | ![screenshot](documentation/readme/features/contact.png) |
| FAQ Page | Site-wide FAQ accordion page to answer common questions. | ![screenshot](documentation/readme/features/faqs.png) |
| 404 Page | Branded 404 page for invalid or broken links. | ![screenshot](documentation/readme/features/404.png) |
| SEO Metadata | Each page includes SEO meta tags (title, description, OG/Twitter). | ![screenshot](documentation/readme/features/seo.png) |
| Marketing Footer | Social media links and newsletter form displayed in footer. | ![screenshot](documentation/readme/features/Footer.png) |
| Facebook Mockup | Social media promotion example with a branded post. | ![screenshot](documentation/readme/features/facebook-mockup.png) |
| Facebook Integration | Connect social media accounts for sharing and login. | ![screenshot](documentation/readme/features/Facebook.png) |
| Stripe Integration | Stripe payment integration for smooth checkout processing. | ![screenshot](documentation/readme/features/stripe.png) |
| User Feedback Messages | Feedback messages on user actions (e.g., adding/removing items). | ![screenshot](documentation/readme/features/user-feedback.png) |
| View Bag | Users can view and manage their shopping cart. | ![screenshot](documentation/readme/features/view-bag.png) |

### Future Features

- **Product Reviews & Ratings**: Users can leave reviews and rate products.
- **Wishlist System**: Users can add/remove products from their wishlist.
- **Sorting Dropdown**: Sort products by price and name.
- **Discount Codes & Vouchers**: Redeemable codes at checkout.
- **Abandoned Cart Recovery**: Email users about uncompleted checkouts.
- **Loyalty Program**: Points-based reward system.
- **Live Chat Support**: Real-time customer support chat.
- **Product Recommendations**: "You might also like" sections.
- **Inventory Alerts**: Notify users when items are back in stock.
- **Shipping Tracking Integration**: Real-time shipping updates.
- **Multi-language/Currency Support**: Internationalization features.
- **Mobile App**: Native app for mobile users.



