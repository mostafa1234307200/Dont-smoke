import streamlit as st
import numpy as np
import cv2
from PIL import Image

# إعداد الصفحة
st.set_page_config(
    page_title="مدرسة الأردن الأساسية المختلطة",
    layout="centered",
    page_icon="🚭",
)

# تنسيق CSS - خلفية جميلة + تنسيق زر الرفع
st.markdown("""
    <style>
        .stApp {
            background-color: #e6f2ff;
            padding: 2rem;
        }
        h1, h3 {
            color: #1b3a57;
            text-align: center;
        }
        .small {
            text-align: center;
            color: #444;
            margin-bottom: 30px;
        }
        .upload-box {
            border: 2px dashed #3399cc;
            border-radius: 10px;
            padding: 20px;
            background-color: #f0f9ff;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# عنوان
st.markdown("<h1>مدرسة الأردن الأساسية المختلطة</h1>", unsafe_allow_html=True)
st.markdown("<h3>كيف ستبدو بعد 30 سنة من التدخين؟</h3>", unsafe_allow_html=True)
st.markdown("<p class='small'>ارفع صورتك لتشاهد تأثير التدخين بشكل واقعي على مظهرك</p>", unsafe_allow_html=True)

# رفع الصورة بشكل أنيق
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("اختر صورة من جهازك أو التقط صورة بالكاميرا", type=["jpg", "jpeg", "png"])
st.markdown('</div>', unsafe_allow_html=True)

# دالة تأثير التدخين
def apply_smoking_effect(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # اصفرار البشرة
    yellow_tint = np.full_like(img, (0, 40, 80))
    img = cv2.addWeighted(img, 0.7, yellow_tint, 0.3, 0)

    # تغميق الشفاه
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lip_mask = cv2.inRange(hsv, (0, 20, 50), (180, 255, 255))
    img[lip_mask > 0] = img[lip_mask > 0] * 0.3

    # إضافة تجاعيد
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    result = cv2.addWeighted(img, 0.85, edges, 0.15, 0)

    return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

# عرض النتيجة
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(img_np, caption="صورتك الأصلية", use_column_width=True)

    with st.spinner("جارٍ تطبيق التأثير..."):
        result = apply_smoking_effect(img_np)
        st.image(result, caption="بعد 30 سنة من التدخين", use_column_width=True)
        st.success("تم تطبيق التأثير بنجاح!")
