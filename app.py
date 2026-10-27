
import streamlit as st
from datetime import date
import io

st.set_page_config(
    page_title="MedPractice Video Studio",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 MedPractice Video Studio")
st.caption("Create healthcare educational scripts and video storyboards.")

with st.sidebar:
    st.header("Video settings")
    platform = st.selectbox(
        "Platform",
        ["Instagram Reel", "YouTube Short", "YouTube Video"],
    )
    audience = st.selectbox(
        "Target audience",
        [
            "General public",
            "Parents and caregivers",
            "Medical students",
            "Healthcare professionals",
        ],
    )
    language = st.selectbox("Language", ["English", "Hindi"])
    tone = st.selectbox(
        "Style",
        ["Friendly and simple", "Professional", "Storytelling"],
    )
    duration = st.select_slider(
        "Video duration",
        options=["30 seconds", "45 seconds", "60 seconds", "3 minutes"],
        value="45 seconds",
    )

topic = st.text_input(
    "What is your healthcare video about?",
    placeholder="e.g. Understanding childhood constipation",
)
key_points = st.text_area(
    "Important points to include (optional)",
    placeholder="Add facts, prevention tips, or points reviewed by a clinician.",
)
call_to_action = st.text_input(
    "Closing message",
    value="Follow for more healthcare education.",
)

def build_script(topic, audience, language, tone, duration, key_points, cta):
    scene_count = {
        "30 seconds": 4,
        "45 seconds": 4,
        "60 seconds": 5,
        "3 minutes": 7,
    }[duration]

    if language == "Hindi":
        hook = f"क्या आप {topic} के बारे में जानना चाहते हैं?"
        intro = f"आइए, {topic} को आसान भाषा में समझते हैं।"
        reminder = "हर व्यक्ति की स्थिति अलग हो सकती है। सही सलाह के लिए योग्य डॉक्टर से संपर्क करें।"
        cta_text = cta
        scene_labels = [
            "शुरुआत", "मुख्य जानकारी", "क्या ध्यान रखें?",
            "व्यावहारिक सुझाव", "कब मदद लें?", "सारांश", "समापन"
        ]
    else:
        hook = f"What should you know about {topic}?"
        intro = f"Let's understand {topic} in simple, practical terms."
        reminder = (
            "This is general health education, not an individual diagnosis. "
            "Consult a qualified clinician for personal advice."
        )
        cta_text = cta
        scene_labels = [
            "Hook", "Introduction", "Key information",
            "Practical guidance", "When to seek help",
            "Key takeaway", "Closing"
        ]

    points = key_points.strip() or (
        "Add clinician-reviewed facts about the topic before publishing."
    )
    duration_seconds = {
        "30 seconds": 30,
        "45 seconds": 45,
        "60 seconds": 60,
        "3 minutes": 180,
    }[duration]
    seconds_per_scene = duration_seconds // scene_count

    narration = [
        hook,
        intro,
        f"Key information about {topic}: {points}",
        f"Practical guidance for {audience}: explain only verified, "
        "topic-appropriate recommendations.",
        reminder,
        f"Remember the most important point about {topic}.",
        cta_text,
    ]

    visuals = [
        f"Clean opening title about {topic}; engaging, non-alarming healthcare graphics.",
        "Simple animated introduction with clear typography and uncluttered layout.",
        "Use a clinician-reviewed infographic to explain the key information.",
        "Show practical steps using friendly icons and accessible visuals.",
        "Show a calm, clear prompt to seek qualified medical care when appropriate.",
        "Summarize the main message using three concise on-screen points.",
        "Display the channel name and closing message.",
    ]

    scenes = []
    for i in range(scene_count):
        scenes.append({
            "number": i + 1,
            "title": scene_labels[i],
            "seconds": seconds_per_scene,
            "narration": narration[i],
            "visual": visuals[i],
        })
    return hook, scenes

if st.button("✨ Generate Script & Storyboard", type="primary"):
    if not topic.strip():
        st.warning("Please enter a healthcare topic first.")
    else:
        hook, scenes = build_script(
            topic, audience, language, tone, duration, key_points, call_to_action
        )
        st.session_state["generated"] = {
            "topic": topic,
            "platform": platform,
            "audience": audience,
            "language": language,
            "tone": tone,
            "duration": duration,
            "hook": hook,
            "scenes": scenes,
        }

if "generated" in st.session_state:
    result = st.session_state["generated"]
    st.divider()
    st.subheader("📝 Your video plan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Scenes", len(result["scenes"]))
    col2.metric("Duration", result["duration"])
    col3.write(f"**Platform**\n\n{result['platform']}")

    st.markdown("### Suggested opening hook")
    st.info(result["hook"])

    full_text = [
        "MEDPRACTICE VIDEO STUDIO — SCRIPT & STORYBOARD",
        f"Topic: {result['topic']}",
        f"Platform: {result['platform']}",
        f"Audience: {result['audience']}",
        f"Language: {result['language']}",
        f"Style: {result['tone']}",
        f"Duration: {result['duration']}",
        "",
    ]

    for scene in result["scenes"]:
        st.markdown(
            f"### Scene {scene['number']}: {scene['title']} "
            f"({scene['seconds']} sec)"
        )
        st.markdown("**Narration**")
        st.write(scene["narration"])
        st.markdown("**Visual direction**")
        st.write(scene["visual"])
        st.markdown("**On-screen caption**")
        st.caption(scene["narration"])
        full_text.extend([
            f"SCENE {scene['number']}: {scene['title']}",
            f"Duration: {scene['seconds']} seconds",
            f"Narration: {scene['narration']}",
            f"Visual: {scene['visual']}",
            f"Caption: {scene['narration']}",
            "",
        ])

    full_text.extend([
        "MEDICAL REVIEW REQUIRED",
        "Verify clinical claims against reliable, current sources and have a "
        "qualified healthcare professional review the content before publication.",
        "This draft is for general education and is not individualized medical advice.",
    ])

    script_file = "\n".join(full_text)
    st.download_button(
        "⬇️ Download script and storyboard (.txt)",
        data=script_file,
        file_name="medpractice_script.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "Version 2 starter: this builds structured drafts from templates. "
    "It does not yet connect to an AI model, generate voiceover, or render MP4 video."
)
