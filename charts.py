import pandas as pd
import re
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def clean_price(price_str):
    # Remove currency symbol and convert to float
    return float(re.sub(r'[^\d]', '', price_str))

def clean_mileage(mileage_str):
    # Remove 'km' and convert to float
    return float(re.sub(r'[^\d]', '', mileage_str))

def create_statistics_charts(df):
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Clean the data
        df['Cena'] = df['Cena'].apply(clean_price)
        df['Przebieg'] = df['Przebieg'].apply(clean_mileage)
        df['Rok produkcji'] = pd.to_numeric(df['Rok produkcji'], errors='coerce')
        
        # Create a subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Rozkład cen samochodów',
                'Zależność ceny od przebiegu',
                '10 najpopularniejszych marek',
                'Rozkład lat produkcji'
            )
        )
        
        # 1. Price Distribution
        fig.add_trace(
            go.Histogram(x=df['Cena'], name='Cena'),
            row=1, col=1
        )
        
        # 2. Mileage vs Price Scatter Plot
        fig.add_trace(
            go.Scatter(
                x=df['Przebieg'],
                y=df['Cena'],
                mode='markers',
                name='Cena vs Przebieg',
                marker=dict(
                    size=8,
                    color=df['Cena'],
                    colorscale='Viridis',
                    showscale=True
                )
            ),
            row=1, col=2
        )
        
        # 3. Most Common Car Brands
        brand_counts = df['Marka'].value_counts().head(10)
        fig.add_trace(
            go.Bar(
                x=brand_counts.values,
                y=brand_counts.index,
                orientation='h',
                name='Marki'
            ),
            row=2, col=1
        )
        
        # 4. Year Distribution
        fig.add_trace(
            go.Histogram(x=df['Rok produkcji'], name='Rok produkcji'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=1000,
            width=1500,
            title_text="Statystyki samochodów",
            showlegend=False,
            template="plotly_white"
        )
        
        # Save the main chart
        stats_chart_filename = f'statistics_charts_{timestamp}.html'
        fig.write_html(stats_chart_filename)
        
        # Create fuel type distribution pie chart
        fuel_counts = df['Rodzaj paliwa'].value_counts()
        fig_fuel = px.pie(
            values=fuel_counts.values,
            names=fuel_counts.index,
            title='Rozkład rodzajów paliwa'
        )
        
        # Save the fuel distribution chart
        fuel_chart_filename = f'fuel_distribution_{timestamp}.html'
        fig_fuel.write_html(fuel_chart_filename)
        
        return stats_chart_filename, fuel_chart_filename
        
    except Exception as e:
        print(f"Błąd podczas tworzenia wykresów: {str(e)}")
        raise 