# Tailwind CSS Setup for MediaDex

This project uses django-tailwind to provide Tailwind CSS styling across all Django apps.

## Architecture

The Tailwind CSS setup is centralized in the `theme` app, which allows all other apps (`login`, `mediadex`, etc.) to use Tailwind classes without individual configuration.

### Structure

```
Backend/
├── theme/                          # Central theme app
│   ├── static_src/                 # Tailwind source files
│   │   ├── src/styles.css         # Main Tailwind CSS file
│   │   ├── package.json           # Node.js dependencies
│   │   └── postcss.config.js      # PostCSS configuration
│   ├── static/css/dist/           # Compiled CSS output
│   └── templates/base.html        # Base template with Tailwind CSS
├── login/                         # Login app
│   └── templates/login.html       # Extends base.html
├── mediadex/                      # Media app
│   └── templates/index.html       # Extends base.html
└── project/settings.py            # Django settings
```

## Configuration

### Settings (project/settings.py)

- `TAILWIND_APP_NAME = 'theme'` - Points to the theme app
- `theme.apps.ThemeConfig` added to `INSTALLED_APPS`
- Base template directory configured: `'DIRS': [BASE_DIR / 'theme' / 'templates']`

### Tailwind Source (theme/static_src/src/styles.css)

- Scans all apps: `@source "../../**/*.{html,py,js}";`
- This automatically includes Tailwind classes from all templates and Python files

## Usage

### For New Apps

1. Create your app templates as usual
2. Extend the base template: `{% extends "base.html" %}`
3. Use Tailwind classes directly in your templates
4. No additional configuration needed!

### Example Template

```html
{% extends "base.html" %} {% block title %}My App - MediaDex{% endblock %} {%
block content %}
<div class="max-w-4xl mx-auto py-8">
  <h1 class="text-4xl font-bold text-gray-900 mb-8">My App</h1>
  <div class="bg-white rounded-lg shadow-md p-6">
    <p class="text-gray-600">Content with Tailwind classes</p>
    <button
      class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
    >
      Button
    </button>
  </div>
</div>
{% endblock %}
```

## Development Commands

### Build CSS (Production)

```bash
cd Backend/theme/static_src
npm run build
```

### Watch for Changes (Development)

```bash
cd Backend/theme/static_src
npm run dev
```

### Install Dependencies

```bash
cd Backend/theme/static_src
npm install
```

## Benefits

1. **Centralized Configuration**: One place to manage Tailwind setup
2. **Automatic Scanning**: All apps are automatically scanned for Tailwind classes
3. **Shared Base Template**: Consistent styling across all apps
4. **Clean Architecture**: Follows Django best practices
5. **Easy Maintenance**: Update Tailwind version in one place

## Adding New Apps

When you create a new Django app:

1. Add it to `INSTALLED_APPS` in settings.py
2. Create templates that extend `base.html`
3. Use Tailwind classes - they'll be automatically included in the build
4. Run `npm run build` to regenerate CSS if needed

No additional Tailwind configuration required!
