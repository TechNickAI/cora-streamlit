import streamlit as st

st.set_page_config(page_title="About: Cora", page_icon="💙", layout="wide")

st.header("Overview")
st.write(
    """
Cora is a heart-centered AI designed to revolutionize human-technology interaction and enhance human potential.
Named after the Latin word for "heart," Cora embodies our commitment to creating AI that is intelligent,
empathetic, ethical, and aligned with human values.

Our vision is to develop an AI that synergizes human creativity with technological capability.
Cora is not just a tool but a partner in your personal and professional growth, aimed at amplifying your effectiveness
and helping you achieve significant improvements in various aspects of your life.
"""
)

st.header("Ethos and Goals")
st.write(
    """
At the core of Cora's development is the philosophy of Heart Centered AI, which seeks to harmonize humanity
and technology. Our goals include:
"""
)
st.markdown(
    """
1. **Empowerment**: Enhance human capabilities, allowing users to focus on high-level strategy and creativity.
2. **Ethical AI**: Ensure AI development remains grounded in empathy and diverse values.
3. **Personalization**: Provide deeply tailored assistance by responsibly leveraging personal data.
4. **Efficiency**: Dramatically improve productivity by handling a wide range of tasks with varying complexity.
5. **Innovation**: Push the boundaries of AI, especially in entrepreneurial and creative domains.
6. **Holistic Growth**: Support users in achieving balance across all aspects of life, not just career or productivity.
"""
)

st.header("Features and Roadmap")
st.subheader("Alpha Release: Foundation (on par with ChatGPT)")
st.write(
    """
- Streamlit-based user interface with text
- Secure user authentication and data handling
- Basic conversation history and context awareness (memory)
- Real-time web searching (Metaphor, Tivaly, Perplexity)
"""
)

st.subheader("Beta Release")
st.write(
    """
- Voice input
- Integration with multiple language models (Claude, GPT-4o, Gemini)
- Intelligent model selection based on query type
- Basic personal data integration (location, preferences)
- Customizable AI agent sophistication levels
- Multi-agent conversations with multiple perspectives
"""
)

st.subheader("Version 1.0 (release to friends)")
st.write(
    """
- Integration with Google services (Calendar, Contacts, Photos)
- Secure access to advanced tools (e.g., Python shell for trusted users)
- Full integration with social media platforms and task management tools
- Advanced conversation memory and context awareness
- Auto-journaling and life-logging capabilities
"""
)

st.subheader("Future Plans")
st.write(
    """
- Comprehensive personal data analysis and insights (AI Chief of Life Officer)
- Integration with signed-in browser profile for logged-in web tasks
- AI-driven project management and execution of complex tasks
- Predictive task completion based on user patterns
- Collaborative AI sessions for multiple users
"""
)
