#!/data/data/com.termux/files/usr/bin/bash

# ============================================
#   SARHAD EXPRESS HR — TERMUX EASY SETUP
#   Sarhad Express Land Transport LLC Dubai
#   Company Code: 574758
# ============================================

GREEN='\033[0;32m'
GOLD='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo ""
echo -e "${GOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║   🚛  SARHAD EXPRESS HR SYSTEM           ║${NC}"
echo -e "${GOLD}║   Dubai UAE  •  Code: 574758             ║${NC}"
echo -e "${GOLD}╚══════════════════════════════════════════╝${NC}"
echo ""

# ── Helper functions ──────────────────────
ok()   { echo -e "${GREEN}✅ $1${NC}"; }
info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
warn() { echo -e "${GOLD}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; }
step() { echo ""; echo -e "${BOLD}${BLUE}━━━ $1 ━━━${NC}"; echo ""; }
ask()  { echo -e "${GOLD}👉 $1${NC}"; }

pause() {
  echo ""
  read -p "$(echo -e ${CYAN})Press ENTER to continue...$(echo -e ${NC})" 
}

check_done() {
  local flag="$HOME/.sarhad_hr/$1"
  [ -f "$flag" ]
}

mark_done() {
  mkdir -p "$HOME/.sarhad_hr"
  touch "$HOME/.sarhad_hr/$1"
}

# ── MENU ─────────────────────────────────
show_menu() {
  clear
  echo ""
  echo -e "${GOLD}╔══════════════════════════════════════════╗${NC}"
  echo -e "${GOLD}║   🚛  SARHAD EXPRESS HR — TERMUX MENU   ║${NC}"
  echo -e "${GOLD}╚══════════════════════════════════════════╝${NC}"
  echo ""
  
  # Show status of each step
  if check_done "step1"; then
    echo -e "  ${GREEN}✅${NC} Step 1 — Update Termux"
  else
    echo -e "  ${RED}⬜${NC} Step 1 — Update Termux"
  fi

  if check_done "step2"; then
    echo -e "  ${GREEN}✅${NC} Step 2 — Install Python & Git"
  else
    echo -e "  ${RED}⬜${NC} Step 2 — Install Python & Git"
  fi

  if check_done "step3"; then
    echo -e "  ${GREEN}✅${NC} Step 3 — Install Python Packages"
  else
    echo -e "  ${RED}⬜${NC} Step 3 — Install Python Packages"
  fi

  if check_done "step4"; then
    echo -e "  ${GREEN}✅${NC} Step 4 — Download HR Project"
  else
    echo -e "  ${RED}⬜${NC} Step 4 — Download HR Project"
  fi

  if check_done "step5"; then
    echo -e "  ${GREEN}✅${NC} Step 5 — Setup Google Credentials"
  else
    echo -e "  ${RED}⬜${NC} Step 5 — Setup Google Credentials"
  fi

  if check_done "step6"; then
    echo -e "  ${GREEN}✅${NC} Step 6 — Configure Sheet ID"
  else
    echo -e "  ${RED}⬜${NC} Step 6 — Configure Sheet ID"
  fi

  echo ""
  echo -e "  ${GREEN}▶  Step 7 — START HR APP${NC}"
  echo -e "  ${CYAN}🔄  Step 8 — Update App (git pull)${NC}"
  echo -e "  ${RED}🔁  Step 9 — Reset All Steps${NC}"
  echo -e "  ${RED}❌  Step 0 — Exit${NC}"
  echo ""
  ask "Choose step number:"
  read -r choice
  run_step "$choice"
}

# ── STEPS ────────────────────────────────

step1_update() {
  step "STEP 1 — UPDATE TERMUX"
  info "Updating Termux packages..."
  pkg update -y && pkg upgrade -y
  if [ $? -eq 0 ]; then
    ok "Termux updated successfully!"
    mark_done "step1"
  else
    err "Update failed. Check internet connection."
  fi
  pause
}

step2_install() {
  step "STEP 2 — INSTALL PYTHON & GIT"
  info "Installing Python, Git, tmux..."
  pkg install -y python git tmux wget
  if [ $? -eq 0 ]; then
    ok "Python version: $(python --version)"
    ok "Git version: $(git --version)"
    ok "All installed!"
    mark_done "step2"
  else
    err "Installation failed."
  fi
  pause
}

step3_pip() {
  step "STEP 3 — INSTALL PYTHON PACKAGES"
  info "Installing Flask, gspread, google-auth..."
  pip install flask gspread google-auth google-auth-oauthlib gunicorn
  if [ $? -eq 0 ]; then
    ok "All Python packages installed!"
    mark_done "step3"
  else
    err "pip install failed."
  fi
  pause
}

step4_download() {
  step "STEP 4 — DOWNLOAD HR PROJECT"
  echo ""
  ask "How do you want to get the project?"
  echo ""
  echo "  1) From GitHub (recommended)"
  echo "  2) From ZIP file in Downloads folder"
  echo ""
  read -r method

  if [ "$method" = "1" ]; then
    echo ""
    ask "Enter your GitHub repo URL:"
    info "Example: https://github.com/fasttarget22/sarhad-hr.git"
    read -r repo_url
    cd "$HOME" || exit
    git clone "$repo_url" sarhad-hr
    if [ $? -eq 0 ]; then
      ok "Project downloaded to ~/sarhad-hr"
      mark_done "step4"
    else
      err "Clone failed. Check URL."
    fi

  elif [ "$method" = "2" ]; then
    info "Looking for ZIP in /sdcard/Download..."
    if ls /sdcard/Download/sarhad-hr*.zip 1>/dev/null 2>&1; then
      ZIP=$(ls /sdcard/Download/sarhad-hr*.zip | head -1)
      ok "Found: $ZIP"
      cd "$HOME" || exit
      unzip -o "$ZIP" -d .
      ok "Extracted to ~/sarhad-hr"
      mark_done "step4"
    else
      err "No sarhad-hr.zip found in /sdcard/Download"
      warn "Copy the ZIP file to your Downloads folder first"
    fi
  fi
  pause
}

step5_creds() {
  step "STEP 5 — SETUP GOOGLE CREDENTIALS"
  echo ""
  info "You need: credentials.json from Google Cloud Console"
  echo ""
  echo -e "  ${CYAN}Instructions:${NC}"
  echo "  1. Go to console.cloud.google.com"
  echo "  2. Create Service Account"
  echo "  3. Download JSON key"
  echo "  4. Save as 'credentials.json' in Downloads"
  echo ""
  
  if ls /sdcard/Download/credentials*.json 1>/dev/null 2>&1; then
    CRED=$(ls /sdcard/Download/credentials*.json | head -1)
    ok "Found: $CRED"
    cp "$CRED" "$HOME/sarhad-hr/credentials.json"
    ok "Copied to ~/sarhad-hr/credentials.json"
    mark_done "step5"
  else
    warn "credentials.json not found in Downloads"
    ask "Have you placed it there? (y/n)"
    read -r ans
    if [ "$ans" = "y" ]; then
      ask "Enter full path to your credentials file:"
      read -r cpath
      cp "$cpath" "$HOME/sarhad-hr/credentials.json"
      ok "Copied!"
      mark_done "step5"
    else
      info "Complete this step after downloading credentials.json"
    fi
  fi
  pause
}

step6_config() {
  step "STEP 6 — CONFIGURE GOOGLE SHEET ID"
  echo ""
  info "Open your Google Sheet in browser"
  info "URL looks like:"
  echo -e "  ${CYAN}https://docs.google.com/spreadsheets/d/${BOLD}SHEET_ID_HERE${NC}/edit"
  echo ""
  ask "Paste your Google Sheet ID here:"
  read -r sheet_id

  if [ -z "$sheet_id" ]; then
    err "Sheet ID cannot be empty"
    pause
    return
  fi

  # Save to .env file
  cat > "$HOME/sarhad-hr/.env" <<EOF
SHEET_ID=$sheet_id
SECRET_KEY=sarhad-express-574758-secret
EOF

  # Also add to bashrc for persistence
  grep -q "SARHAD_SHEET_ID" "$HOME/.bashrc" || cat >> "$HOME/.bashrc" <<EOF

# Sarhad Express HR
export SHEET_ID="$sheet_id"
export SECRET_KEY="sarhad-express-574758-secret"
EOF

  source "$HOME/.bashrc"
  ok "Sheet ID saved!"
  ok "Config saved to ~/sarhad-hr/.env"
  mark_done "step6"
  pause
}

step7_start() {
  step "STEP 7 — START HR APP"

  # Check prerequisites
  if ! check_done "step4"; then
    err "Please complete Step 4 first (Download Project)"
    pause; return
  fi
  if ! check_done "step5"; then
    warn "Step 5 not done (credentials.json missing)"
    ask "Continue anyway? (y/n)"
    read -r ans
    [ "$ans" != "y" ] && return
  fi
  if ! check_done "step6"; then
    warn "Step 6 not done (Sheet ID not configured)"
    ask "Continue anyway? (y/n)"
    read -r ans
    [ "$ans" != "y" ] && return
  fi

  # Load env
  if [ -f "$HOME/sarhad-hr/.env" ]; then
    export $(cat "$HOME/sarhad-hr/.env" | xargs)
  fi

  cd "$HOME/sarhad-hr" || exit

  echo ""
  ask "Run mode?"
  echo "  1) Normal (see logs)"
  echo "  2) Background with tmux (keep running)"
  read -r mode

  if [ "$mode" = "2" ]; then
    tmux new-session -d -s sarhad-hr "cd $HOME/sarhad-hr && export SHEET_ID='$SHEET_ID' && export SECRET_KEY='$SECRET_KEY' && python app.py"
    echo ""
    ok "App running in background!"
    ok "Open browser: http://localhost:5000"
    echo ""
    info "To view logs:  tmux attach -t sarhad-hr"
    info "To stop:       tmux kill-session -t sarhad-hr"
  else
    echo ""
    ok "Starting Sarhad Express HR..."
    ok "Open browser: http://localhost:5000"
    echo ""
    info "Press Ctrl+C to stop"
    echo ""
    python app.py
  fi
  pause
}

step8_update() {
  step "STEP 8 — UPDATE APP"
  cd "$HOME/sarhad-hr" || exit
  info "Pulling latest code from GitHub..."
  git pull
  if [ $? -eq 0 ]; then
    ok "App updated!"
    info "Restart the app to apply changes (Step 7)"
  else
    err "Update failed. Check internet."
  fi
  pause
}

step9_reset() {
  step "STEP 9 — RESET ALL STEPS"
  warn "This will reset all step checkmarks (not delete files)"
  ask "Are you sure? (y/n)"
  read -r ans
  if [ "$ans" = "y" ]; then
    rm -rf "$HOME/.sarhad_hr"
    ok "All steps reset!"
  fi
  pause
}

# ── ROUTER ───────────────────────────────
run_step() {
  case "$1" in
    1) step1_update ;;
    2) step2_install ;;
    3) step3_pip ;;
    4) step4_download ;;
    5) step5_creds ;;
    6) step6_config ;;
    7) step7_start ;;
    8) step8_update ;;
    9) step9_reset ;;
    0) echo ""; ok "Goodbye! 🚛"; echo ""; exit 0 ;;
    *) warn "Invalid choice" ;;
  esac
  show_menu
}

# ── START ────────────────────────────────
show_menu
