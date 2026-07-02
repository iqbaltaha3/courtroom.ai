"""Application constants - colors, sizes, and static values."""

# ========== APP METADATA ==========
APP_NAME = "MyPeshkar"
APP_TAGLINE = "Never Miss a Tareekh."
APP_PAGE_TITLE = f"{APP_NAME} - {APP_TAGLINE}"
APP_PAGE_ICON = "⚖"

# ========== COLOR PALETTE - Rich Wood Theme ==========
# Primary Colors
COLOR_PRIMARY_WOOD = "#704214"      # Rich walnut brown
COLOR_DARK_WOOD = "#4A2C1A"         # Espresso shadows
COLOR_LIGHT_WOOD = "#FFFBF5"        # Cream ivory background
COLOR_WARM_CREAM = "#F5E6D3"        # Warm cream

# Accent Colors
COLOR_GOLD_LIGHT = "#D4A574"        # Honey/gold highlights
COLOR_GOLD_SHADOW = "#6B5344"       # Old shadow (keeping for compat)

# Neutral Colors
COLOR_TEXT_PRIMARY = "#2c3e50"      # Dark text
COLOR_TEXT_SECONDARY = "#666"       # Medium gray
COLOR_TEXT_LIGHT = "#7f8c8d"        # Light gray
COLOR_BORDER_LIGHT = "#e1e8ed"      # Light borders
COLOR_BG_LIGHT = "#f5f7fa"          # Light background

# Verdict Colors
COLOR_VERDICT_GOOD = "#27ae60"      # Green
COLOR_VERDICT_BAD = "#e74c3c"       # Red
COLOR_VERDICT_NEUTRAL = "#f39c12"   # Amber

# ========== SIZING CONSTANTS ==========
BORDER_RADIUS_SMALL = "4px"
BORDER_RADIUS_MEDIUM = "8px"
BORDER_RADIUS_LARGE = "16px"

PADDING_SMALL = "0.5rem"
PADDING_MEDIUM = "1.5rem"
PADDING_LARGE = "2.5rem"

BORDER_WIDTH_THIN = "1px"
BORDER_WIDTH_MEDIUM = "2px"
BORDER_WIDTH_ACCENT = "6px"

# ========== SHADOW CONSTANTS ==========
SHADOW_SMALL = "0 4px 12px rgba(70, 42, 26, 0.15)"
SHADOW_MEDIUM = "0 6px 20px rgba(70, 42, 26, 0.2)"
SHADOW_LARGE = "0 12px 32px rgba(70, 42, 26, 0.2)"
SHADOW_INSET = "inset 0 1px 0 rgba(212, 165, 116, 0.3)"

# ========== FONT CONSTANTS ==========
FONT_FAMILY_MAIN = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
FONT_FAMILY_HEADER = "'Brush Script MT', 'Lucida Handwriting', cursive"

# ========== LAYOUT CONSTANTS ==========
LAYOUT_WIDTH = "wide"
MIN_HEIGHT_CARD = "140px"
MIN_HEIGHT_DEBATE = "250px"

# ========== API CONSTANTS ==========
API_TIMEOUT_SECONDS = 30
API_MAX_RETRIES = 3
API_RETRY_DELAY_SECONDS = 2

# ========== AGENT NAMES ==========
AGENT_CASE_MANAGER = "case_manager"
AGENT_LEGAL_RESEARCHER = "legal_researcher"
AGENT_PROSECUTOR = "prosecutor"
AGENT_DEFENSE = "defense"
AGENT_JUDGE = "judge"
AGENT_REPORTER = "reporter"
AGENT_CONSULTANT = "consultant"
AGENT_WEB_SEARCH = "web_search"
