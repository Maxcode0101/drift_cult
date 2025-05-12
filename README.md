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
| User Registration & Authentication | Users can register, log in, and log out via Django Allauth. Includes email confirmation and welcome email. | ![screenshot](documentation/readme/features/1_user_authentication_and_authorization.png) |
| Product Browsing & Search | Products can be browsed by category or searched via keyword. | ![screenshot](documentation/readme/features/2_product_browsing_and_search.png) |
| Shopping Cart | Users can add products to cart, change quantities, or remove items. Cart updates in real time. | ![screenshot](documentation/readme/features/3_shopping_cart_and_checkout.png) |
| Checkout Process | Logged-in users can complete checkout using Stripe. Guest users are prompted to log in or register. | ![screenshot](documentation/readme/features/3_shopping_cart_and_checkout.png) |
| Stripe Payment Integration | Secure payment using Stripe Checkout Sessions. Includes quantity-aware line items and user email. | ![screenshot](documentation/readme/features/4_payment_processing.png) |
| Order Management (User) | Users can view order history and details from their profile. Orders include product names, sizes, and total paid. | ![screenshot](documentation/readme/features/5_order_management.png) |
| Order Management (Admin) | Staff can view, update, or delete orders via the admin dashboard. Bulk status actions and email notifications are available. | ![screenshot](documentation/readme/features/6_admin_dashboard.png) |
| Admin Product Management | Superusers can create, update, and delete products, and manage product sizes and stock levels. | ![screenshot](documentation/readme/features/6_admin_dashboard.png) |
| SEO Optimization | Meta tags are dynamically injected per page for SEO and social sharing (OpenGraph, Twitter cards, etc.). | ![screenshot](documentation/readme/features/7_seo_and_marketing.png) |
| Newsletter Signup | AJAX-based email capture with feedback messages. Confirmation email is sent using a branded HTML template. | ![screenshot](documentation/readme/features/7_seo_and_marketing.png) |
| Responsive Design | Fully mobile-first responsive design using Bootstrap 4. Optimized for mobile, tablet, and desktop views. | ![screenshot](documentation/readme/features/8_responsive_design.png) |
| Wishlist System | Logged-in users can add/remove products from their wishlist. Products in wishlist are highlighted. | ![screenshot](documentation/readme/features/9_wishlist.png) |
| Custom 404 Page | Branded 404 page if users visit a broken or invalid URL. | ![screenshot](documentation/readme/features/404.png) |
| Contact Form | Users can submit their name, email, and a message. Emails are sent to service@driftcult.art. | ![screenshot](documentation/readme/features/contact.png) |
| Footer with Social Media | Links to Instagram, Facebook, TikTok, and Twitter are provided in the footer for visibility and branding. | ![screenshot](documentation/readme/features/7_seo_and_marketing.png) |

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



