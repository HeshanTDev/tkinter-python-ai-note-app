"""
config/theme.py
Centralized design token registry.
All colors, fonts, sizing used across the UI are defined here.
Prevents style duplication and makes theme changes a one-line edit.
"""

# ─── Color Palette ──────────────────────────────────────────────────────────

COLORS = {
    # Brand accent
    "accent":           "#3b82f6",       # blue-500
    "accent_hover":     "#2563eb",       # blue-600
    "accent_dark":      "#1d4ed8",       # blue-700

    # Danger
    "danger":           "#ef4444",       # red-500
    "danger_hover":     "#dc2626",       # red-600

    # Success
    "success":          "#22c55e",       # green-500
    "success_hover":    "#16a34a",       # green-600

    # Surfaces  (light / dark)
    "bg_sidebar":       ("#f4f4f5", "#111111"),
    "bg_list":          ("#f9fafb", "#141414"),
    "bg_editor":        ("#ffffff", "#141414"),
    "bg_card":          ("#ffffff", "#1c1c1e"),
    "bg_card_active":   ("#eff6ff", "#1e3a5f"),
    "bg_input":         ("#ffffff", "#1e1e1e"),
    "bg_ai_bar":        ("#f3f4f6", "#1c1c1e"),
    "bg_modal":         ("#f9fafb", "#1c1c1e"),

    # Borders
    "border":           ("#e5e7eb", "#2a2a2a"),
    "border_active":    ("#3b82f6", "#2563eb"),

    # Text
    "text_primary":     ("#111827", "#f9fafb"),
    "text_secondary":   ("#6b7280", "#9ca3af"),
    "text_muted":       ("#9ca3af", "#6b7280"),
    "text_white":       "#ffffff",

    # Hover states
    "hover_nav":        ("#e5e7eb", "#1f1f1f"),
    "hover_card":       ("#f3f4f6", "#252525"),
    "hover_ai_btn":     ("#f3f4f6", "#2a2a2a"),
    "hover_ai_btn_bg":  ("#e5e7eb", "#333333"),

    # Tag colors
    "tag_bg":           ("#dbeafe", "#1e3a5f"),
    "tag_text":         ("#1d4ed8", "#93c5fd"),
}

# ─── Typography ─────────────────────────────────────────────────────────────

FONT_FAMILY = "Inter"

FONTS = {
    "brand":    ("Inter", 22, "bold"),
    "h1":       ("Inter", 28, "bold"),
    "h2":       ("Inter", 20, "bold"),
    "h3":       ("Inter", 16, "bold"),
    "body_lg":  ("Inter", 15, "normal"),
    "body":     ("Inter", 14, "normal"),
    "body_sm":  ("Inter", 13, "normal"),
    "caption":  ("Inter", 11, "normal"),
    "mono":     ("Consolas", 14, "normal"),
}

# ─── Sizing / Spacing ────────────────────────────────────────────────────────

RADIUS = {
    "xs":   4,
    "sm":   6,
    "md":   10,
    "lg":   12,
    "xl":   16,
}

SPACING = {
    "xs":   4,
    "sm":   8,
    "md":   16,
    "lg":   24,
    "xl":   32,
}
