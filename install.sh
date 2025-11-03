#!/data/data/com.termux/files/usr/bin/bash
# =======================================================
# 🔥 PROJECT MOKSHA - The Silent Installer v1.0 🔥
# =======================================================

PREFIX="/data/data/com.termux/files/usr"
DEST_PATH="$PREFIX/bin/moksha"
SOURCE_URL="https://raw.githubusercontent.com/SachinSolunke/FRP---BYPASS/main/moksha.py"

# Step 1: Zaroori auzaar chupchaap install karna
(
    pkg update -y > /dev/null 2>&1
    pkg install python pv android-tools ncurses-utils -y > /dev/null 2>&1
    pip install rich > /dev/null 2>&1
) &> /dev/null

# Step 2: Mukhya astra (Python script) ko download karna aur progress dikhana
echo "🔥 Moksha Astra ko aapke shastragar mein shaamil kiya ja raha hai..."
curl -# -L "$SOURCE_URL" -o "$DEST_PATH"

# Step 3: Astra ko shakti dena
chmod +x "$DEST_PATH"

# Antim Sandesh
echo ""
echo "✅ Safalta! Moksha Astra ab taiyar hai."
echo "Ise istemal karne ke liye, terminal band karke dobara kholen aur kahin se bhi yeh command likhein:"
echo ""
echo "   moksha"
echo ""
