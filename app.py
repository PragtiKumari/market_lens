import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from streamlit_lottie import st_lottie
import json
from io import BytesIO
from PIL import Image


# ✅ Load image from 'figures' folder using absolute path
def load_figure(filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, 'figures', filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Figure '{filename}' not found at {path}")
    return Image.open(path)

# ✅ Show figure with caption & fallback warning
def show_figure(filename, caption=""):
    try:
        image = load_figure(filename)
        st.image(image, caption=caption, use_column_width=True)
    except FileNotFoundError as e:
        st.warning(f"⚠️ {e}")


st.subheader()
show_figure("figure_1.png", "Sales Forecasting")
show_figure("figure_2.png", "Customer Segmentation")
show_figure("figure_3.png", "Price Sensitivity")
show_figure("figure_4.png", "CLV Prediction")



# -- Page Config --
st.set_page_config(page_title="MarketLens Dashboard", layout="wide")

# -- Load Lottie Animation --
def load_lottiefile(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None

# -- Show Saved Figures --
def show_figure(filename, caption=""):
    path = os.path.join("figures", filename)
    if os.path.exists(path):
        image = Image.open(path)
        st.image(image, caption=caption, use_column_width=True)
    else:
        st.warning(f"⚠️ Figure '{filename}' not found.")

# -- Utility: CSV Download Button --
def download_button(df, filename):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    st.download_button("📥 Download CSV", data=buffer.getvalue(), file_name=filename, mime='text/csv')

# -- Load Lottie --
lottie_dashboard = load_lottiefile("animations/dashboard.json")

# -- Navigation Sidebar
page = st.sidebar.radio("🧭 Navigate to:", [
    "Home",
    "Sales Forecast",
    "Customer Segmentation",
    "Competitor Analysis",
    "Price Sensitivity",
    "Customer Lifetime Value",
    "Ad Campaign Effectiveness",
    "Extra Insights"
])

# -- Push Contact Info to Bottom
st.sidebar.markdown("<div style='height:130px;'></div>", unsafe_allow_html=True)

# -- Contact Info with Real Links
st.sidebar.markdown("""
    <hr style='border:0.5px solid #999; margin:15px 0;'>
    <div style='font-size:13px; opacity:0.85;'>
        📧 <a href="mailto:btech15110.22@bitmesra.ac.in" style="text-decoration: none; color: inherit;"><b>btech15110.22@bitmesra.ac.in</b></a><br>
        📞 <a href="tel:+918102215574" style="text-decoration: none; color: inherit;"><b>+91-8102215574</b></a>
    </div>
""", unsafe_allow_html=True)


# ========== HOME ==========
if page == "Home":
    # Properly styled title
    st.markdown("<h1 style='font-size:36px; font-weight:700; margin-bottom:25px;'>🔍 MarketLens: Market Research & Sales Dashboard</h1>", unsafe_allow_html=True)

    # Optional: Lottie animation
    if lottie_dashboard:
        st_lottie(lottie_dashboard, speed=1, reverse=False, loop=True, quality="high", height=60)

    # Beautifully styled description
    st.markdown("""
        <div style="font-size:17px; line-height:1.7; margin-top:10px; margin-bottom:30px;">
            <p>
                In today’s fast-changing markets, especially in regions with diverse customer behavior, new businesses often struggle with scattered, disconnected data.  
                They rely on gut-feel marketing, generic pricing strategies, and guesswork — which frequently results in wasted resources, missed opportunities, and stagnant growth.\n
         This project is developed specifically to bridge that gap.\n
         By combining customer segmentation, pricing analysis, competition study, lifetime value modeling, and campaign performance — all in one comprehensive dashboard — 
                decision-makers gain a clear, actionable view of what’s really happening. Whether launching a new product, expanding to new markets, or aiming to optimize marketing spend, 
                this tool empowers to make faster, more confident, data-driven decisions.
                That’s what makes this project an actual need. It’s a response to a real problem new businesses face.\n
         Now, with this tool, they won’t have to...
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Clean feature list with spacing
    st.markdown("""
        <div style="font-size:20px; font-weight:600; margin-bottom:10px;">📊 Key Features</div>
        <ul style="font-size:16px; line-height:1.8; margin-left:20px;">
            <li>📈 <b>Sales Forecasting</b> (30-day)</li>
            <li>🧠 <b>Customer Segmentation</b></li>
            <li>🥊 <b>Competitor Analysis</b></li>
            <li>💸 <b>Price Sensitivity</b></li>
            <li>💰 <b>Customer Lifetime Value (CLV)</b></li>
            <li>📢 <b>Ad Campaign Effectiveness</b></li>
            <li>💡 <b>Extra Insights</b></li>
        </ul>
    """, unsafe_allow_html=True)


# ========== SALES FORECAST ==========
elif page == "Sales Forecast":
    st.header("📈 Sales Forecast")
    with st.spinner("Loading sales forecast data..."):
        try:
            df = pd.read_csv('data/final_output.csv')
            st.dataframe(df)
            download_button(df, "sales_forecast.csv")

            selected_columns = ['ZN', 'SB', 'TAX', 'MARZA', 'total_sales']
            for column in selected_columns:
                if column in df.columns:
                    st.subheader(f"📊 Forecast for {column.upper()}")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(df[column], label=column, color='teal')
                    ax.set_title(f"30-Day Forecast: {column.upper()}")
                    ax.grid(True)
                    st.pyplot(fig)

                    st.markdown(f"""
                    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
                    This line graph shows the predicted sales trend for <b>{column.upper()}</b> over the next 30 days.  
                    For businesses in India, especially small and medium enterprises, understanding these trends helps in managing stock, planning promotions, and avoiding overproduction.  
                    Accurate forecasting ensures better cash flow and customer satisfaction by meeting demand without delay.
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")

    st.subheader("30-Day Forecast for ZN")
    show_figure("figure_3.png", "ZN: 30-Day Forecast")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    This chart visualizes the 30-day sales forecast for the ZN product segment.  
    In the Indian market, where demand can vary due to festivals, seasons, or regional preferences, such forecasts help businesses prepare inventory and marketing strategies effectively. ZN refers to a specific zone or behavioral customer segment, grouped by traits like region, shopping patterns, or engagement level. The 30-day forecast for ZN helps you predict demand, campaign responsiveness, and sales behavior in this distinct cluster. Whether you're planning targeted promotions or adjusting logistics, this gives you the clarity to act fast and profit smart.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("30-Day Forecast for SB")
    show_figure("figure_4.png", "SB: 30-Day Forecast")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    The SB forecast graph indicates how this product line’s sales are expected to change soon.  
    Retailers in India often face challenges from sudden market shifts; reliable predictions aid in keeping products available when customers want them most. SB stands for Small Business customers, one of the most crucial buyer groups in many industries. This forecast offers a forward-looking view into how sales from this group are likely to shift. Use it to tailor B2B outreach, improve service cycles, or plan capacity based on demand. Predict small biz momentum — and serve them better before they even ask.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("30-Day Forecast for TAX") 
    show_figure("figure_5.png", "TAX: 30-Day Forecast")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    This forecast highlights the sales projection for TAX, crucial for budgeting and resource allocation.  
    Indian businesses can use these insights to optimize their supply chain and improve operational efficiency. This module anticipates how tax-driven sales (e.g., seasonal purchases around tax deadlines or filings) might trend over the next month. It’s ideal for businesses dealing in finance, consultancy, or software tools. Stay ahead of cyclical surges, align marketing with demand spikes, and plan for peak revenue windows without scrambling last-minute.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("30-Day Forecast for MARZA")
    show_figure("figure_6.png", "MARZA: 30-Day Forecast")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    The MARZA product’s predicted sales pattern is shown here, offering a window into future customer demand.  
    This assists Indian entrepreneurs in making smarter decisions about promotions and stock replenishment, especially during peak shopping periods. MARZA reflects a high-margin product category or a profitable customer cluster you’ve defined. With this forecast, you get predictive insights on how sales in this juicy segment will perform — helping you focus on the most lucrative areas. Great for inventory decisions, premium campaigns, and high-ROI planning.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Total Sales Over Time")
    show_figure("figure_7.png", "Total Sales Over Time")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    This figure displays the overall sales trend combining all products.  
    Monitoring total sales helps Indian business owners see bigger market movements, spot growth opportunities, and plan long-term strategies to stay competitive. It lets you trace your sales evolution month-by-month or week-by-week. Instantly spot patterns, dips, and peaks to shape better decisions. Use it to evaluate past campaigns, budget effectively, or boost your pitch decks with real numbers. It's not just a chart — it's a growth compass.
    </div>
    """, unsafe_allow_html=True)


# ========== CUSTOMER SEGMENTATION ==========
elif page == "Customer Segmentation":
    st.header("🧠 Customer Segmentation")
    with st.spinner("Loading segmentation data..."):
        try:
            df = pd.read_csv("data/processed/customer_segments.csv")
            st.dataframe(df.head())
            download_button(df, "customer_segments.csv")

            if 'segment' in df.columns:
                st.subheader("Segment Distribution")
                fig, ax = plt.subplots()
                ax.pie(df['segment'].value_counts(), labels=df['segment'].value_counts().index,
                       autopct='%1.1f%%', colors=sns.color_palette("pastel"))
                ax.axis('equal')
                st.pyplot(fig)

                st.markdown("""
                <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
                This pie chart shows how customers are divided into different segments based on their buying behavior.  
                For Indian businesses, understanding these segments is crucial for tailoring marketing campaigns, creating personalized offers, and improving customer satisfaction.  
                It helps save costs by targeting the right audience instead of a generic approach.
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")

    st.subheader("Customer Segments : Recency vs Monetary")
    show_figure("figure_2.png", "Customer Segments: Monetary vs Recency")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    This plot visualizes customer segments by how recently and how much they spend.  
    retailers can use this to identify loyal customers and those at risk of churning, helping design reward programs that boost retention and lifetime value. This chart breaks down customer behavior based on how recently they bought and how much they spent. Want to know who your MVPs are? Or who needs a reactivation nudge? Done. It empowers precision targeting so you don’t waste a single campaign rupee.
    </div>
    """, unsafe_allow_html=True)


# ========== COMPETITOR ANALYSIS ==========
elif page == "Competitor Analysis":
    st.header("🥊 Competitor Analysis")
    with st.spinner("Loading competitor data..."):
        try:
            df = pd.read_csv("data/processed/competitor_data.csv")
            st.dataframe(df.head())
            download_button(df, "competitor_data.csv")

            if 'Price' in df.columns and 'Sales' in df.columns:
                st.subheader("Price vs Sales")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(data=df, x='Price', y='Sales', ax=ax)
                ax.set_title('Price vs Sales')
                ax.grid(True)
                st.pyplot(fig)

                st.markdown("""
                <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
                This scatter plot compares competitors' product prices with their sales volume.  
                For Indian companies, analyzing competitor pricing helps set competitive prices without losing profit, ensuring they attract price-sensitive customers while maintaining market share. Here you can see how changes in price affect your actual sales volume. It's the cheat code for discovering the optimal pricing zone. Whether you're launching new products or adjusting existing ones, you’ll know exactly when you're hitting the sweet spot — and when you’re leaving money on the table.
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")


# ========== PRICE SENSITIVITY ==========
elif page == "Price Sensitivity":
    st.header("💸 Price Sensitivity Analysis")
    with st.spinner("Loading price sensitivity data..."):
        try:
            df = pd.read_csv("data/processed/price_sensitivity.csv")
            st.dataframe(df.head())
            download_button(df, "price_sensitivity.csv")

            if 'price' in df.columns and 'sensitivity_score' in df.columns:
                st.subheader("Price vs Sensitivity Score")
                fig, ax = plt.subplots()
                sns.lineplot(data=df, x='price', y='sensitivity_score', marker='o', ax=ax)
                ax.set_title('Price vs Sensitivity Score')
                ax.grid(True)
                st.pyplot(fig)

                st.markdown("""
                <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
                This line chart illustrates how customer sensitivity changes with product price.  
                In the Indian market, where buyers are often highly price-conscious, such insights guide businesses to set optimal prices that maximize sales without losing customers.
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")

    st.subheader("Price sensitivity (Regression)")
    show_figure("figure_12.png", "Clicks vs Price")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    This regression chart shows the relationship between product price and ad clicks.  
    Indian marketers can use this to understand how pricing affects online interest, helping design smarter digital campaigns that convert better. Understand how your customers react to price changes, backed by data, not gut feel. This module uses regression models to help you raise prices without losing volume — or discount strategically to maximize revenue. No more pricing guesswork, just profits backed by math.
    </div>
    """, unsafe_allow_html=True)


# ========== CUSTOMER LIFETIME VALUE ==========
elif page == "Customer Lifetime Value":
    st.header("💰 Customer Lifetime Value")
    with st.spinner("Loading CLV data..."):
        try:
            df = pd.read_csv("data/processed/clv.csv")
            st.dataframe(df.head())
            download_button(df, "clv.csv")

            if 'clv' in df.columns and 'customer_id' in df.columns:
                st.subheader("Top 10 Customers by CLV")
                top_customers = df.sort_values(by='clv', ascending=False).head(10)
                fig, ax = plt.subplots()
                sns.barplot(data=top_customers, x='clv', y='customer_id', palette='Blues_d', ax=ax)
                ax.set_title('Top Customers by CLV')
                st.pyplot(fig)

                st.markdown("""
                <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
                This bar chart ranks the top 10 customers based on their lifetime value.  
                Indian businesses can focus their retention and loyalty programs on these high-value customers, maximizing profits and encouraging repeat purchases.
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")

    #  Showing extra figure: CLV by Segment

    st.subheader("Customer segments based on CLV")
    show_figure("figure_10.png", "CLV by Segment: Comparing Average Lifetime Value Across Customer Groups")

    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-top:10px;">
   This segmentation lets you focus on customers who’ll stick around and spend more over time. These insights help you retain valuable customers longer, prioritize your ad spend, and build loyalty strategies that deliver compounding returns. Invest smarter, not harder.  \n
    You can use this insight to:
    <ul>
        <li> Personalize offers and experiences for your best segments</li>
        <li> Run targeted marketing campaigns only where it counts</li>
        <li> Prioritize budget and retention efforts to maximize ROI</li>
    </ul>
    Instead of treating every customer the same, this helps you invest smartly in the segments that actually matter. 🎯
    </div>
    """, unsafe_allow_html=True)



# ========== AD CAMPAIGN EFFECTIVENESS ==========
elif page == "Ad Campaign Effectiveness":
    st.header("📢 Ad Campaign Effectiveness")
    show_figure("figure_9.png", "Feature Importance for Click Prediction")
    st.markdown("""
    <div style="font-size:16px; line-height:1.5; margin-bottom:20px;">
    This figure shows which features (like user age, device type, ad position and other factors) most influence whether an ad gets clicked.  
    For Indian digital marketers, understanding these factors is essential to optimize ad targeting, reduce wasted spend, and increase campaign ROI. Finally, a dashboard that shows which campaigns are actually driving results. See your ad spend vs impact in real terms — sales, clicks, conversions, the whole shebang. Kill the campaigns that don’t work, double down on the ones that do, and become a marketing genius with zero guesswork.
    </div>
    """, unsafe_allow_html=True)


# ========== EXTRA INSIGHTS ==========
elif page == "Extra Insights":
    st.markdown("<h1 style='font-size:36px;'>💡 Extra Insights</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:18px; line-height:1.8; margin-top:10px; margin-bottom:40px;">
        This dashboard is more than just charts and predictions — it's designed to support smart decision-making based on real market behavior.  
        By combining multiple data sources like sales, pricing trends, and customer preferences, we help businesses focus on what matters most.  
        Here's a breakdown of the most valuable insights uncovered through this project:
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="line-height:1.8; font-size:16px;">

    <h2 style="font-size:24px;">📌 Understanding the Big Picture</h2>
    <p>
        Instead of analyzing metrics in isolation, this dashboard combines behavior, pricing, market response, and performance into one unified strategy.  
        This connected view is essential for businesses to identify long-term patterns, seasonal trends, and emerging opportunities, especially in dynamic markets where customer preferences shift frequently.
    </p>

    <h2 style="font-size:22px;">👥 Customer Segmentation: Personalizing for Diversity</h2>
    <p>
        Every customer is different — some buy often, others only during sales, and some respond better to certain product categories.  
        With proper segmentation, businesses can identify these patterns and offer more personalized experiences.  
        For example, customers in Tier-1 cities may value convenience and brand loyalty, while those in Tier-2/3 cities might be more price-sensitive and promo-driven.  
        This helps companies design smarter campaigns and avoid a one-size-fits-all approach.
    </p>

    <h2 style="font-size:22px;">💸 Price Sensitivity: Finding the Sweet Spot</h2>
    <p>
        Pricing has a direct impact on conversion — and understanding how much a price change affects customer behavior is crucial.  
        Our analysis helps identify the exact price bands where customers are most likely to purchase.  
        This is especially important in competitive product categories like mobile accessories or packaged foods, where even ₹10 difference can affect buying decisions.  
        Businesses can use this to optimize pricing strategy without hurting profit margins.
    </p>

    <h2 style="font-size:22px;">🏁 Competitor Analysis: Staying Ahead</h2>
    <p>
        Businesses don't operate in isolation — customers are constantly comparing options.  
        Through competitor performance and pricing analysis, companies can spot gaps and areas where they’re underperforming.  
        For instance, if a competitor is gaining more traction in certain regions or product lines, this insight can prompt a relook into marketing or bundling strategies.  
        Staying informed about the market helps businesses make proactive moves.
    </p>

    <h2 style="font-size:22px;">📈 Customer Lifetime Value: Prioritizing What Matters</h2>
    <p>
        Some customers bring far more value over time than others.  
        Our CLV model helps identify which customers are worth investing in for loyalty and retention.  
        For example, frequent buyers of high-margin items should be targeted with exclusive deals or early access offers.  
        In a growing online shopping environment, long-term relationships reduce acquisition costs and increase revenue stability.
    </p>

    <h2 style="font-size:22px;">🎯 Ad Campaign Effectiveness: Smarter Spending</h2>
    <p>
        Digital ads can be expensive — and spending without targeting leads to wasted budgets.  
        By analyzing which customer attributes lead to higher ad clicks, businesses can improve targeting strategies.  
        For instance, promoting fashion items to users who’ve shown interest in lifestyle content at peak hours yields better results than broad-based campaigns.  
        This boosts ROI and ensures that campaigns hit the right audience at the right time.
    </p>

    </div>
    """, unsafe_allow_html=True)




# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
    <div style="text-align:center;">
        <h4>MarketLens • All-in-One Market & Sales Research Dashboard • 2025</h4>
        <p>💖 Built by Pragati Kumari 💖</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .reportview-container {
            padding: 0 2rem 2rem 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        .stRadio > div {
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)


