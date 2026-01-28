"""
HTML Generator for Browser-based Calculator System.
Creates an interactive Omni Calculator-style interface.
"""

import json
from .calculator_data import CALCULATORS


def generate_calculator_html() -> str:
    """Generate the complete HTML for the calculator system."""

    # Convert calculator data to JSON for JavaScript
    calc_json = json.dumps(CALCULATORS, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engineering Calculator Suite - ITU Racing</title>
    <style>
        :root {{
            --bg-dark: #0a0a0a;
            --bg-medium: #141414;
            --bg-light: #1e1e1e;
            --bg-elevated: #282828;
            --text-white: #ffffff;
            --text-light: #e0e0e0;
            --text-gray: #888888;
            --accent: #3d9970;
            --accent-hover: #2d7a5a;
            --border: #2a2a2a;
            --border-light: #3a3a3a;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--bg-dark);
            color: var(--text-white);
            min-height: 100vh;
        }}

        .header {{
            background: var(--bg-medium);
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
        }}

        .header p {{
            color: var(--text-gray);
            font-size: 14px;
        }}

        .search-container {{
            max-width: 600px;
            margin: 15px auto 0;
        }}

        .search-input {{
            width: 100%;
            padding: 12px 20px;
            border: 1px solid var(--border-light);
            border-radius: 25px;
            background: var(--bg-light);
            color: var(--text-white);
            font-size: 16px;
            outline: none;
        }}

        .search-input:focus {{
            border-color: var(--accent);
        }}

        .main-container {{
            display: flex;
            max-width: 1600px;
            margin: 0 auto;
            min-height: calc(100vh - 120px);
        }}

        .sidebar {{
            width: 280px;
            background: var(--bg-medium);
            border-right: 1px solid var(--border);
            padding: 20px;
            position: sticky;
            top: 120px;
            height: calc(100vh - 120px);
            overflow-y: auto;
        }}

        .sidebar h2 {{
            font-size: 14px;
            color: var(--text-gray);
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .category-btn {{
            display: flex;
            align-items: center;
            width: 100%;
            padding: 12px 15px;
            background: transparent;
            border: none;
            color: var(--text-light);
            cursor: pointer;
            font-size: 14px;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: all 0.2s;
            text-align: left;
        }}

        .category-btn:hover {{
            background: var(--bg-light);
        }}

        .category-btn.active {{
            background: var(--accent);
            color: white;
        }}

        .category-icon {{
            font-size: 20px;
            margin-right: 12px;
            width: 24px;
            text-align: center;
        }}

        .content {{
            flex: 1;
            padding: 30px;
        }}

        .category-header {{
            margin-bottom: 30px;
        }}

        .category-header h2 {{
            font-size: 28px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .category-header p {{
            color: var(--text-gray);
        }}

        .calculators-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}

        .calc-card {{
            background: var(--bg-medium);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .calc-card:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
        }}

        .calc-card h3 {{
            font-size: 16px;
            margin-bottom: 8px;
        }}

        .calc-card p {{
            color: var(--text-gray);
            font-size: 13px;
        }}

        /* Calculator Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}

        .modal.active {{
            display: flex;
        }}

        .modal-content {{
            background: var(--bg-medium);
            border-radius: 16px;
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            border: 1px solid var(--border);
        }}

        .modal-header {{
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            background: var(--bg-medium);
        }}

        .modal-header h2 {{
            font-size: 20px;
        }}

        .close-btn {{
            background: none;
            border: none;
            color: var(--text-gray);
            font-size: 24px;
            cursor: pointer;
            padding: 5px;
        }}

        .close-btn:hover {{
            color: var(--text-white);
        }}

        .modal-body {{
            padding: 25px;
        }}

        .calc-description {{
            color: var(--text-gray);
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border);
        }}

        .input-section, .output-section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 12px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }}

        .input-group {{
            margin-bottom: 15px;
        }}

        .input-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .input-unit {{
            color: var(--text-gray);
        }}

        .input-field {{
            width: 100%;
            padding: 12px 15px;
            background: var(--bg-light);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-white);
            font-size: 16px;
            outline: none;
        }}

        .input-field:focus {{
            border-color: var(--accent);
        }}

        .output-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 15px;
            background: var(--bg-light);
            border-radius: 8px;
            margin-bottom: 10px;
        }}

        .output-label {{
            color: var(--text-gray);
            font-size: 14px;
        }}

        .output-value {{
            font-size: 18px;
            font-weight: 600;
            color: var(--accent);
        }}

        .output-unit {{
            color: var(--text-gray);
            font-size: 14px;
            margin-left: 5px;
        }}

        /* Stats counter */
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            padding: 15px;
            background: var(--bg-light);
            border-bottom: 1px solid var(--border);
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 24px;
            font-weight: bold;
            color: var(--accent);
        }}

        .stat-label {{
            font-size: 12px;
            color: var(--text-gray);
        }}

        /* Responsive */
        @media (max-width: 900px) {{
            .main-container {{
                flex-direction: column;
            }}
            .sidebar {{
                width: 100%;
                height: auto;
                position: static;
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                padding: 10px;
            }}
            .sidebar h2 {{
                width: 100%;
            }}
            .category-btn {{
                flex: 0 0 auto;
                width: auto;
                padding: 8px 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Engineering Calculator Suite</h1>
        <p>ITU Racing | Formula Student</p>
        <div class="search-container">
            <input type="text" class="search-input" placeholder="Search calculators..." id="searchInput">
        </div>
    </div>

    <div class="stats">
        <div class="stat-item">
            <div class="stat-number" id="totalCalcs">0</div>
            <div class="stat-label">Calculators</div>
        </div>
        <div class="stat-item">
            <div class="stat-number" id="totalCategories">0</div>
            <div class="stat-label">Categories</div>
        </div>
    </div>

    <div class="main-container">
        <nav class="sidebar">
            <h2>Categories</h2>
            <div id="categoryList"></div>
        </nav>

        <main class="content">
            <div class="category-header" id="categoryHeader">
                <h2><span id="categoryIcon"></span> <span id="categoryTitle">Select a Category</span></h2>
                <p id="categoryDescription">Choose a category from the sidebar to view calculators</p>
            </div>
            <div class="calculators-grid" id="calculatorsGrid"></div>
        </main>
    </div>

    <div class="modal" id="calcModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Calculator</h2>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <p class="calc-description" id="modalDescription"></p>
                <div class="input-section">
                    <div class="section-title">Inputs</div>
                    <div id="inputsContainer"></div>
                </div>
                <div class="output-section">
                    <div class="section-title">Results</div>
                    <div id="outputsContainer"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const CALCULATORS = {calc_json};

        let currentCalc = null;

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            renderCategories();
            updateStats();

            // Select first category
            const firstCat = Object.keys(CALCULATORS)[0];
            if (firstCat) selectCategory(firstCat);

            // Search functionality
            document.getElementById('searchInput').addEventListener('input', handleSearch);
        }});

        function updateStats() {{
            let totalCalcs = 0;
            Object.values(CALCULATORS).forEach(cat => {{
                totalCalcs += Object.keys(cat.calculators).length;
            }});
            document.getElementById('totalCalcs').textContent = totalCalcs;
            document.getElementById('totalCategories').textContent = Object.keys(CALCULATORS).length;
        }}

        function renderCategories() {{
            const container = document.getElementById('categoryList');
            container.innerHTML = '';

            Object.entries(CALCULATORS).forEach(([key, cat]) => {{
                const btn = document.createElement('button');
                btn.className = 'category-btn';
                btn.innerHTML = `<span class="category-icon">${{cat.icon}}</span>${{key}}`;
                btn.onclick = () => selectCategory(key);
                btn.dataset.category = key;
                container.appendChild(btn);
            }});
        }}

        function selectCategory(categoryKey) {{
            // Update active button
            document.querySelectorAll('.category-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.dataset.category === categoryKey);
            }});

            const category = CALCULATORS[categoryKey];
            if (!category) return;

            // Update header
            document.getElementById('categoryIcon').textContent = category.icon;
            document.getElementById('categoryTitle').textContent = categoryKey;
            document.getElementById('categoryDescription').textContent = category.description;

            // Render calculators
            const grid = document.getElementById('calculatorsGrid');
            grid.innerHTML = '';

            Object.entries(category.calculators).forEach(([calcKey, calc]) => {{
                const card = document.createElement('div');
                card.className = 'calc-card';
                card.innerHTML = `
                    <h3>${{calc.name}}</h3>
                    <p>${{calc.description}}</p>
                `;
                card.onclick = () => openCalculator(categoryKey, calcKey);
                grid.appendChild(card);
            }});
        }}

        function handleSearch(e) {{
            const query = e.target.value.toLowerCase();
            if (!query) {{
                const firstCat = Object.keys(CALCULATORS)[0];
                if (firstCat) selectCategory(firstCat);
                return;
            }}

            const results = [];
            Object.entries(CALCULATORS).forEach(([catKey, cat]) => {{
                Object.entries(cat.calculators).forEach(([calcKey, calc]) => {{
                    if (calc.name.toLowerCase().includes(query) ||
                        calc.description.toLowerCase().includes(query)) {{
                        results.push({{ catKey, calcKey, calc, icon: cat.icon }});
                    }}
                }});
            }});

            // Update header
            document.getElementById('categoryIcon').textContent = '🔍';
            document.getElementById('categoryTitle').textContent = 'Search Results';
            document.getElementById('categoryDescription').textContent = `Found ${{results.length}} calculators`;

            // Render results
            const grid = document.getElementById('calculatorsGrid');
            grid.innerHTML = '';

            results.forEach(({{ catKey, calcKey, calc, icon }}) => {{
                const card = document.createElement('div');
                card.className = 'calc-card';
                card.innerHTML = `
                    <h3>${{icon}} ${{calc.name}}</h3>
                    <p>${{calc.description}}</p>
                `;
                card.onclick = () => openCalculator(catKey, calcKey);
                grid.appendChild(card);
            }});
        }}

        function openCalculator(categoryKey, calcKey) {{
            const calc = CALCULATORS[categoryKey].calculators[calcKey];
            currentCalc = calc;

            document.getElementById('modalTitle').textContent = calc.name;
            document.getElementById('modalDescription').textContent = calc.description;

            // Render inputs
            const inputsContainer = document.getElementById('inputsContainer');
            inputsContainer.innerHTML = '';

            calc.inputs.forEach(input => {{
                const group = document.createElement('div');
                group.className = 'input-group';
                group.innerHTML = `
                    <div class="input-label">
                        <span>${{input.label}}</span>
                        <span class="input-unit">${{input.unit}}</span>
                    </div>
                    <input type="number" class="input-field"
                           id="input_${{input.id}}"
                           value="${{input.default}}"
                           step="any"
                           oninput="calculate()">
                `;
                inputsContainer.appendChild(group);
            }});

            // Render outputs
            const outputsContainer = document.getElementById('outputsContainer');
            outputsContainer.innerHTML = '';

            calc.outputs.forEach(output => {{
                const row = document.createElement('div');
                row.className = 'output-row';
                row.innerHTML = `
                    <span class="output-label">${{output.label}}</span>
                    <span>
                        <span class="output-value" id="output_${{output.id}}">-</span>
                        <span class="output-unit">${{output.unit}}</span>
                    </span>
                `;
                outputsContainer.appendChild(row);
            }});

            document.getElementById('calcModal').classList.add('active');
            calculate();
        }}

        function closeModal() {{
            document.getElementById('calcModal').classList.remove('active');
            currentCalc = null;
        }}

        function calculate() {{
            if (!currentCalc) return;

            // Gather input values
            const values = {{}};
            currentCalc.inputs.forEach(input => {{
                const el = document.getElementById(`input_${{input.id}}`);
                values[input.id] = parseFloat(el.value) || 0;
            }});

            // Calculate outputs
            currentCalc.outputs.forEach(output => {{
                try {{
                    // Create formula with actual values
                    let formula = output.formula;
                    Object.entries(values).forEach(([key, val]) => {{
                        formula = formula.replace(new RegExp(`\\\\b${{key}}\\\\b`, 'g'), val);
                    }});

                    const result = eval(formula);
                    const el = document.getElementById(`output_${{output.id}}`);

                    if (isNaN(result) || !isFinite(result)) {{
                        el.textContent = '-';
                    }} else if (Math.abs(result) >= 10000 || (Math.abs(result) < 0.001 && result !== 0)) {{
                        el.textContent = result.toExponential(3);
                    }} else {{
                        el.textContent = parseFloat(result.toPrecision(6));
                    }}
                }} catch (e) {{
                    document.getElementById(`output_${{output.id}}`).textContent = 'Error';
                }}
            }});
        }}

        // Close modal on escape
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeModal();
        }});

        // Close modal on background click
        document.getElementById('calcModal').addEventListener('click', (e) => {{
            if (e.target.id === 'calcModal') closeModal();
        }});
    </script>
</body>
</html>'''

    return html


def save_calculator_html(filepath: str = None) -> str:
    """Save the calculator HTML to a file and return the path."""
    import os
    import tempfile

    if filepath is None:
        # Create in temp directory
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, 'itu_racing_calculator.html')

    html = generate_calculator_html()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return filepath


def open_calculator_in_browser() -> str:
    """Generate HTML and open in browser."""
    import webbrowser

    filepath = save_calculator_html()
    webbrowser.open(f'file://{filepath}')
    return filepath
