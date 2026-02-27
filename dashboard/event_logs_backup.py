# History UI

import streamlit as st
import pandas as pd
from database.db import get_connection
from config.settings import EVENT_LABELS

# Custom CSS for professional styling with beige background
st.markdown("""
    <style>
    /* Professional Color Palette */
    :root {
        --primary-blue: #1565C0;
        --primary-dark: #0D47A1;
        --primary-light: #42A5F5;
        --secondary-teal: #00897B;
        --secondary-light: #4DB6AC;
        --accent-orange: #FF6F00;
        --accent-amber: #FFA726;
        --success-green: #2E7D32;
        --success-light: #4CAF50;
        --danger-red: #C62828;
        --danger-light: #EF5350;
        --warning-yellow: #F57C00;
        --neutral-dark: #424242;
        --neutral-medium: #757575;
        --neutral-light: #BDBDBD;
        --bg-primary: #F5F7FA;
        --bg-secondary: #E3F2FD;
        --bg-accent: #E1F5FE;
    }
    
    /* Background - Beige/Mild Colors */
    .main .block-container {
        background: linear-gradient(135deg, #FAF8F3 0%, #F5F1E8 100%);
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F5F1E8 0%, #FAF8F3 100%);
    }
    
    /* Main Headers */
    .main-header {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    /* Sub Headers */
    .sub-header {
        font-size: 1.15rem;
        color: var(--neutral-medium);
        margin-bottom: 2.5rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: var(--primary-blue);
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 0.75rem;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

def show_event_logs():
    st.markdown('<h1 class="main-header">📜 History</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Complete log of all detected events and system alerts</p>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ About Event Logs", expanded=False):
        st.markdown("""
        **Event History:**
        - All detected events are automatically logged with timestamps
        - Includes prediction type, confidence level, and alert messages
        - Events are sorted by most recent first
        - Only non-normal events (impacts, crashes, shifts) are logged
        
        **Use Cases:**
        - Review historical incidents
        - Analyze detection patterns
        - Monitor system performance over time
        """)
    
    st.markdown("---")

    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM events ORDER BY timestamp DESC", conn)
        conn.close()

        if df.empty:
            st.info("""
            **No Events Logged Yet**
            
            The event log is currently empty. Events will appear here once the system detects:
            - Mild impacts
            - Severe crashes
            - Container shifts
            
            Normal operation events are not logged to keep the history focused on significant events.
            """)
            return

        # Handle NULL values and format the dataframe
        # Fill NULL predicted_label with -1 (Unknown) for display, but handle conversion carefully
        if "predicted_label" in df.columns:
            df["predicted_label"] = pd.to_numeric(df["predicted_label"], errors='coerce').fillna(-1).astype(int)
        else:
            df["predicted_label"] = -1
        
        # Create Event Type mapping with fallback for NULL/unknown
        event_labels_with_unknown = EVENT_LABELS.copy()
        event_labels_with_unknown[-1] = "Unknown"
        df["Event Type"] = df["predicted_label"].map(event_labels_with_unknown).fillna("Unknown")
        
        # Handle NULL confidence
        if "confidence" in df.columns:
            df["confidence"] = pd.to_numeric(df["confidence"], errors='coerce').fillna(0.0)
        else:
            df["confidence"] = 0.0
        
        df["Confidence"] = df["confidence"].apply(lambda x: f"{float(x):.1%}" if pd.notna(x) and x is not None else "N/A")
        
        # Format timestamp - handle both string and datetime formats
        if "timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")
            df["Timestamp"] = df["Timestamp"].fillna("Unknown")
        else:
            df["Timestamp"] = "Unknown"
        
        # Handle alert column
        if "alert" not in df.columns:
            df["alert"] = "N/A"
        df["alert"] = df["alert"].fillna("N/A")
        
        # Reorder columns
        display_df = df[["Timestamp", "Event Type", "Confidence", "alert"]].copy()
        display_df.columns = ["Timestamp", "Event Type", "Confidence", "Alert Message"]
        
        # Display statistics - safely handle filtering
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Events", len(df))
        with col2:
            try:
                severe_count = len(df[df["predicted_label"] == 2]) if "predicted_label" in df.columns else 0
            except Exception:
                severe_count = 0
            st.metric("Severe Crashes", severe_count, delta=None)
        with col3:
            try:
                mild_count = len(df[df["predicted_label"] == 1]) if "predicted_label" in df.columns else 0
            except Exception:
                mild_count = 0
            st.metric("Mild Impacts", mild_count, delta=None)
        with col4:
            try:
                shift_count = len(df[df["predicted_label"] == 3]) if "predicted_label" in df.columns else 0
            except Exception:
                shift_count = 0
            st.metric("Container Shifts", shift_count, delta=None)
        
        st.markdown("---")
        st.markdown("### 📋 Event Details")
        
        # Display dataframe with better formatting
        # Use TextColumn for Timestamp since it's already formatted as string
        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
            column_config={
                "Timestamp": st.column_config.TextColumn(
                    "Timestamp",
                    width="medium"
                ),
                "Event Type": st.column_config.TextColumn(
                    "Event Type",
                    width="medium"
                ),
                "Confidence": st.column_config.TextColumn(
                    "Confidence",
                    width="small"
                ),
                "Alert Message": st.column_config.TextColumn(
                    "Alert Message",
                    width="large"
                )
            }
        )
        
        # Export option
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Event Log (CSV)",
            data=csv,
            file_name=f"event_log_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download the complete event log as a CSV file"
        )
        
    except Exception as e:
        import traceback
        st.error(f"⚠️ Error loading event history: {str(e)}")
        with st.expander("🔍 Error Details", expanded=False):
            st.code(traceback.format_exc(), language="python")
        st.info("""
        **Troubleshooting Steps:**
        1. Ensure the database file exists at `database/events.db`
        2. Check that the database schema is properly initialized
        3. Verify database permissions
        4. Try restarting the application
        """)
