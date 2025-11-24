#!/usr/bin/env bash

# Exit on error
set -e

# ---- Input Check ----
if [ -z "$1" ]; then
    echo "Usage: $0 <service_name>"
    exit 1
fi

SERVICE_NAME="$1"
TITLE_CASE="$(echo "$SERVICE_NAME" | sed -E 's/(^|_)(.)/\ U\2/g')"

# ---- Directory Structure ----
echo "Creating directory tree for service: $SERVICE_NAME"

# Template directories
mkdir -p "templates/$SERVICE_NAME"

# Static directories
mkdir -p "static/$SERVICE_NAME/images"
mkdir -p "static/$SERVICE_NAME/js"
mkdir -p "static/$SERVICE_NAME/styles"

# ---- Template Files ----
cat > "templates/$SERVICE_NAME/home.html" <<EOF
<!DOCTYPE html>
{% extends '$SERVICE_NAME/base.html' %}

{% block header %}

<h1>$TITLE_CASE</h1>

{% endblock %}


{% block content %}

<section>
    <p>$TITLE_CASE</p>
</section>

{% endblock %}
EOF

cat > "templates/$SERVICE_NAME/base.html" <<EOF
<!DOCTYPE HTML>
<html>
    <head>
        <title>$TITLE_CASE</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='base.css') }}">
        <link rel="stylesheet" href="{{ url_for('static', filename='$SERVICE_NAME/styles/styles.css') }}">
        <style>

        </style>
    </head>
    <body>
        {% include '$SERVICE_NAME/nav_menu.html' %}
        <section id="sleeve">
            <section class="content">
                <header id="header">
                    <!-- That up there ^ -->
                    {% for message in get_flashed_messages() %}
                    <div class="flash">{{ message }}</div>
                    {% endfor %}
                    <!-- Page specific header -->
                    {% block header %}{% endblock %}
                </header>
                <main>
                    <!-- Page specific content -->
                    {% block content %}{% endblock %}
                </main>
            </section>
            <footer>
                <!-- Modularize -->
                <h3 class="left_foot">Whale Shark $TITLE_CASE(c)</h3>
                <h3 class="right_foot">2025</h3>
            </footer>
        </section>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="{{ url_for('static', filename='index.js')  }}"></script>
    </body>
</html>
EOF

cat > "templates/$SERVICE_NAME/nav_menu.html" <<EOF
{% extends 'nav_m.html' %}

{% block nav_menu %}
<a href="" class="glass">New Button</a>
<a href="" class="glass">New Button</a>
{% endblock %}
EOF

# ---- Static Files ----
cat > "static/$SERVICE_NAME/js/index.js" <<EOF
// JavaScript for $SERVICE_NAME
console.log("Loaded $TITLE_CASE frontend");
EOF

cat > "static/$SERVICE_NAME/styles/styles.css" <<EOF
/* Styles for $TITLE_CASE */
body {
    background-image: none;
}
EOF

# ---- Complete ----
echo "Service '$SERVICE_NAME' directory tree created successfully."