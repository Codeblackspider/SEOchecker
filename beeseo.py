import requests
from bs4 import BeautifulSoup
import time

# Define terminal color codes
class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ORANGE = "\033[33m"  # Custom orange color
    CYAN = "\033[96m"  # Custom cyan color
    MAGENTA = "\033[95m"  # Custom magenta color
    LIGHT_BLUE = "\033[94m"  # Light blue color
    LIGHT_GREEN = "\033[92m"  # Light green color
    RESET = "\033[0m"

# ASCII Art for the tool title with gradient
ascii_art = [
    "   ____               _____",
    "  / __ )___  ___     / ___/___  ____ ",
    " / __  / _ \\/ _ \\    \\__ \\/ _ \\/ __ \\",
    "/ /_/ /  __/  __/   ___/ /  __/ /_/ /",
    "/_____/\\___/\\___/   /____/\\___/\\____/"
]

# Function to print ASCII art with gradient
def print_ascii_art_with_gradient():
    gradient_colors = [
        Colors.LIGHT_BLUE,
        Colors.CYAN,
        Colors.GREEN,
        Colors.YELLOW,
        Colors.ORANGE,
        Colors.RED
    ]
    for i, line in enumerate(ascii_art):
        color = gradient_colors[i % len(gradient_colors)]
        print(f"{color}{line}{Colors.RESET}")

# Function to check meta tags
def check_meta_tags(soup):
    title_tag = soup.title.string if soup.title else 'No Title Tag'
    description = soup.find("meta", attrs={"name": "description"})
    keywords = soup.find("meta", attrs={"name": "keywords"})

    return {
        "Title": title_tag,
        "Description": description["content"] if description else "No Meta Description",
        "Keywords": keywords["content"] if keywords else "No Meta Keywords"
    }

# Function to check page load time
def check_page_load_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return round(end_time - start_time, 2)

# Function to check keyword density
def check_keyword_density(soup, keyword):
    text = soup.get_text().lower()
    words = text.split()
    keyword_count = text.count(keyword.lower())
    return round((keyword_count / len(words)) * 100, 2)

# Function to check broken links
def check_broken_links(soup):
    broken_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Filter out unwanted links like '/', '#', and mailto links
        if href in ['/', '#'] or href.startswith('mailto:') or href.startswith('javascript:'):
            continue
        try:
            response = requests.head(href, timeout=5)
            if response.status_code >= 400:
                broken_links.append(href)
        except requests.RequestException:
            broken_links.append(href)
    return broken_links

# Function to check mobile friendliness
def check_mobile_friendly(soup):
    viewport = soup.find("meta", attrs={"name": "viewport"})
    return viewport is not None

# Function to check image alt tags
def check_image_alt_tags(soup):
    images_without_alt = []
    for img in soup.find_all('img'):
        if not img.get('alt'):
            images_without_alt.append(img.get('src'))
    return images_without_alt

# Function to provide SEO suggestions
def seo_suggestions(meta_tags, load_time, keyword_densities, broken_links, is_mobile_friendly, images_without_alt):
    suggestions = []
    if meta_tags['Title'] == 'No Title Tag':
        suggestions.append("Add a title tag to your page.")
    if meta_tags['Description'] == 'No Meta Description':
        suggestions.append("Add a meta description to your page.")
    for keyword, density in keyword_densities.items():
        if density < 0.5:
            suggestions.append(f"Increase the keyword density for '{keyword}' to improve SEO.")
    if broken_links:
        suggestions.append("Fix broken links on your page.")
    if not is_mobile_friendly:
        suggestions.append("Make your page mobile-friendly.")
    if images_without_alt:
        suggestions.append("Add alt text to all images.")
    return suggestions

# Function to print SEO suggestions in a green box
def print_suggestions_box(suggestions):
    if suggestions:
        print(f"\n{Colors.GREEN}" + "-" * 70)
        for suggestion in suggestions:
            print(f"| {suggestion.ljust(66)} |")
        print("-" * 70 + f"{Colors.RESET}\n")

# Main SEO checker function
def seo_checker():
    # Print the ASCII art title with gradient
    print_ascii_art_with_gradient()
    
    # Display the website link
    print(f"{Colors.GREEN}Visit our website: {Colors.BLUE}https://www.fontbees.store/{Colors.RESET}\n")
    
    # Prompt user for input
    url = input(f"{Colors.GREEN}Enter the URL of the blog: {Colors.RESET}")
    keywords = input(f"{Colors.GREEN}Enter the keywords to check density (comma-separated): {Colors.RESET}")
    keyword_list = [k.strip() for k in keywords.split(',')]

    print(f"\n{Colors.YELLOW}Checking SEO for:{Colors.RESET} {Colors.BLUE}{url}{Colors.RESET}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize score and max_score
    score = 0
    max_score = 6  # Number of checks

    # Meta Tags
    meta_tags = check_meta_tags(soup)
    print(f"{Colors.YELLOW}Title:{Colors.RESET} {Colors.BLUE}{meta_tags['Title']}{Colors.RESET}")
    print(f"{Colors.YELLOW}Description:{Colors.RESET} {Colors.BLUE}{meta_tags['Description']}{Colors.RESET}")
    print(f"{Colors.YELLOW}Keywords:{Colors.RESET} {Colors.BLUE}{meta_tags['Keywords']}{Colors.RESET}")
    if meta_tags['Title'] != 'No Title Tag' and meta_tags['Description'] != 'No Meta Description':
        score += 1

    # Page Load Time
    load_time = check_page_load_time(url)
    print(f"{Colors.YELLOW}Page load time:{Colors.RESET} {Colors.BLUE}{load_time} seconds{Colors.RESET}")
    if load_time < 3:  # Arbitrary threshold for page load time
        score += 1

    # Keyword Density
    keyword_densities = {}
    for keyword in keyword_list:
        density = check_keyword_density(soup, keyword)
        keyword_densities[keyword] = density
        print(f"{Colors.YELLOW}Keyword Density for '{keyword}':{Colors.RESET} {Colors.BLUE}{density}%{Colors.RESET}")
        if density > 0.5:  # Arbitrary threshold for keyword density
            score += 1

    # Broken Links
    broken_links = check_broken_links(soup)
    if broken_links:
        print(f"{Colors.YELLOW}Broken Links Found:{Colors.RESET} {Colors.BLUE}{broken_links}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}No Broken Links Found{Colors.RESET}")
        score += 1

    # Mobile Friendliness
    is_mobile_friendly = check_mobile_friendly(soup)
    print(f"{Colors.YELLOW}Mobile-Friendly:{Colors.RESET} {Colors.BLUE}{'Yes' if is_mobile_friendly else 'No'}{Colors.RESET}")
    if is_mobile_friendly:
        score += 1

    # Image Alt Text
    images_without_alt = check_image_alt_tags(soup)
    if images_without_alt:
        print(f"{Colors.YELLOW}Images without Alt Text:{Colors.RESET} {Colors.BLUE}{images_without_alt}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}All images have Alt Text{Colors.RESET}")
        score += 1

    # Calculate SEO score percentage
    seo_score = (score / max_score) * 100

    # Determine the color based on the SEO score
    if seo_score >= 75:
        bar_color = Colors.GREEN
    elif 50 <= seo_score < 75:
        bar_color = Colors.ORANGE
    else:
        bar_color = Colors.RED

    # Display the final SEO score with a progress bar
    print(f"\n{bar_color}Total SEO Score: {seo_score}%{Colors.RESET}")
    progress_bar_length = 40
    filled_length = int(progress_bar_length * seo_score // 100)
    bar = f"{bar_color}{'█' * filled_length}{Colors.RESET}{'░' * (progress_bar_length - filled_length)}"
    print(f"{bar} {seo_score}%")

    # Display SEO suggestions in a green box
    suggestions = seo_suggestions(meta_tags, load_time, keyword_densities, broken_links, is_mobile_friendly, images_without_alt)
    print_suggestions_box(suggestions)

# Run the SEO checker
seo_checker()
