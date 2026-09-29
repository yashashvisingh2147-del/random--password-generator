# SecurePass – Random Strong Password Generator

## 1. Problem Statement

Weak and predictable passwords can reduce the security of user accounts. Users often create passwords that are short, repetitive, or lack a combination of different character types.

**SecurePass** addresses this problem by providing a Python-based web application that generates strong random passwords using Python's `secrets` module. The application allows users to customize password length and character types and provides a password-strength analysis feature.

The application does not store or transmit generated passwords.

---

## 2. Scope of the Project

The scope of SecurePass includes:

* Generating random passwords using Python's `secrets` module.
* Supporting uppercase letters, lowercase letters, numbers, and special symbols.
* Allowing password lengths from 8 to 32 characters.
* Providing an option to exclude ambiguous characters such as `l`, `I`, `1`, `O`, and `0`.
* Providing an option to avoid repeated characters.
* Generating multiple passwords.
* Analysing password strength based on length, character types, uniqueness, and repeated characters.
* Providing a Flask-based web interface and API endpoints.
* Providing password generation and password-strength checking through the application.

The project does not store passwords or provide account-management functionality.

---

## 3. Target Users

SecurePass is intended for:

* Students learning cybersecurity and Python.
* Users who need randomly generated passwords.
* Users who want to check the basic strength characteristics of a password.
* Beginners studying web application development with Flask.

---

## 4. High-Level Features

### 4.1 Secure Password Generation

Uses Python's `secrets` module to generate random passwords.

### 4.2 Custom Password Configuration

Users can select:

* Password length
* Uppercase letters
* Lowercase letters
* Numbers
* Symbols
* No repeated characters
* Exclusion of ambiguous characters

### 4.3 Multiple Password Generation

The application can generate multiple unique passwords in a single request.

### 4.4 Password Strength Analysis

The application analyses:

* Password length
* Uppercase characters
* Lowercase characters
* Numbers
* Symbols
* Character uniqueness
* Repeated characters

It returns a score, percentage, label, and criteria.

### 4.5 Flask Web Application

The project uses Flask to provide the web interface and API endpoints.

---

## 5. Major Project Modules

### Module 1 – Password Generator

**File:** `password_generator.py`

Responsible for:

* Building the character set.
* Generating individual passwords.
* Generating batches of passwords.
* Applying user-selected password options.

### Module 2 – Password Strength Analyzer

**File:** `strength_analyzer.py`

Responsible for:

* Checking password characteristics.
* Calculating the strength score.
* Assigning a strength category.
* Returning password criteria.

### Module 3 – Flask Application

**File:** `app.py`

Responsible for:

* Running the web application.
* Displaying the main interface.
* Receiving password-generation requests.
* Providing password-strength checking through the `/check` endpoint.
* Providing password-generation through the `/generate` endpoint.

---

## 6. Technologies Used

* Python
* Flask
* `secrets` module
* `string` module
* HTML templates
* JSON-based API communication

---

## 7. Expected Outcome

The expected outcome is a functional web-based password generator that can create customizable random passwords and analyse their basic strength characteristics through a simple Flask application.
