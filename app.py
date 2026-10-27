
import streamlit as st
import re

st.set_page_config(
    page_title="MedPractice Video Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 MedPractice Video Studio")
st.caption("Healthcare scripts and faceless video planning")

topic = st.text_input(
    "Healthcare topic",
    placeholder="Example: Childhood constipation"
)

platform = st.selectbox(
    "Target platform",
    [
        "Instagram Reel / YouTube Short (9:16)",
        "YouTube Video (16:9)"
    ]
)

audience = st.selectbox(
    "Target audience",
    [
        "General public",
        "Parents and caregivers",
        "Medical students",
        "Healthcare professionals"
    ]
)

if st.button("Generate Script + Storyboard", type="primary"):
    if not topic.strip():
        st.warning("Please enter a healthcare topic.")
    else:
        scenes = [
            {
                "title": "Scene 1 — Hook",
                "duration": 5,
                "narration": (
                    f"What should you know about {topic}? "
                    "Let's break down the essentials."
                ),
                "visual": (
                    f"Display the title '{topic}' with clean, "
                    "professional healthcare-themed graphics."
                ),
            },
            {
                "title": "Scene 2 — Explanation",
                "duration": 10,
                "narration": (
                    f"First, understand the basics of {topic}. "
                    "Use clear, simple language to explain the "
                    "main concept and why it matters."
                ),
                "visual": (
                    "Show a simple labelled illustration or "
                    "educational diagram relevant to the topic."
                ),
            },
            {
                "title": "Scene 3 — Key Information",
                "duration": 10,
                "narration": (
                    "Next, focus on the most important facts, "
                    "practical information, and common questions. "
                    "Check all clinical statements against "
                    "reliable medical sources."
                ),
                "visual": (
                    "Present three concise educational points "
                    "with readable captions and simple icons."
                ),
            },
            {
                "title": "Scene 4 — Safety and Closing",
                "duration": 5,
                "narration": (
                    "If you have concerns, seek advice from "
                    "a qualified healthcare professional. "
                    "Follow for more evidence-informed health education."
                ),
                "visual": (
                    "Show a calm closing screen with a medical "
                    "review reminder and channel branding."
                ),
            },
        ]

        output = [
            "MEDPRACTICE VIDEO STUDIO",
            "=" * 35,
            f"Topic: {topic}",
            f"Audience: {audience}",
            f"Platform: {platform}",
            "Target duration: 30 seconds",
            "",
            "FULL NARRATION SCRIPT",
            "-" * 25,
        ]

        for scene in scenes:
            output.extend([
                "",
                scene["title"],
                f"Duration: {scene['duration']} seconds",
                f"NARRATION: {scene['narration']}",
                f"VISUAL DIRECTION: {scene['visual']}",
            ])

        output.extend([
            "",
            "PRE-PUBLICATION REVIEW",
            "- Verify clinical claims using reliable medical references.",
            "- Check recommendations, warning signs and safety wording.",
            "- Review narration timing and caption readability.",
            "- Check image and audio usage rights.",
            "- Obtain qualified clinical review before publication.",
            "",
            "This is a draft for general education, not individual medical advice."
        ])

        script_text = "\n".join(output)

        st.session_state["script_text"] = script_text
        st.session_state["scenes"] = scenes
        st.session_state["topic"] = topic

if "script_text" in st.session_state:
    st.divider()
    st.subheader("Your narration script and storyboard")

    for scene in st.session_state["scenes"]:
        with st.expander(
            f"{scene['title']} — {scene['duration']} seconds",
            expanded=True
        ):
            st.markdown("**Voiceover**")
            st.write(scene["narration"])
            st.markdown("**Visual direction**")
            st.write(scene["visual"])

    safe_topic = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        st.session_state["topic"]
    ).strip("_")[:60] or "healthcare_topic"

    st.download_button(
        "⬇️ Download Script + Storyboard (.txt)",
        data=st.session_state["script_text"],
        file_name=f"{safe_topic}_script.txt",
        mime="text/plain",
        type="primary"
    )

    st.info(
        "This version uses a built-in template, not an AI model. "
        "Review medical accuracy, safety advice, and timing before publishing."
    )
