# ============================================================
# ỨNG DỤNG TÍNH SỐ MÔN B/C CÓ THỂ ĐẠT ĐỂ GPA CUỐI KHÓA >= 3.8
# Chạy trực tiếp trên Google Colab
# ============================================================
import gradio as gr


# ============================================================
# CÁC THÔNG SỐ CỐ ĐỊNH CỦA CHƯƠNG TRÌNH
# ============================================================

TONG_TIN_CHI = 137
TIN_CHI_MON = 3
TIN_CHI_KHOA_LUAN = 9
GPA_MUC_TIEU = 3.8

# Khóa luận được giả định đạt A
DIEM_KHOA_LUAN = 4.0


# ============================================================
# HÀM TẠO THẺ MINH HỌA
# ============================================================

def tao_the(diem, so_mon, loai, mau, nen):
    return f"""
    <div style="
        background: {nen};
        border: 2px solid {mau};
        border-radius: 18px;
        padding: 18px 12px;
        text-align: center;
        min-height: 120px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    ">
        <div style="
            font-size: 42px;
            font-weight: 800;
            color: {mau};
            line-height: 1;
        ">
            {diem}
        </div>

        <div style="
            font-size: 15px;
            font-weight: 600;
            margin-top: 8px;
            color: #333;
        ">
            {loai}
        </div>

        <div style="
            font-size: 24px;
            font-weight: 700;
            color: {mau};
            margin-top: 8px;
        ">
            {so_mon}
        </div>

        <div style="
            font-size: 13px;
            color: #666;
        ">
            học phần
        </div>
    </div>
    """


# ============================================================
# HÀM TÍNH TOÁN
# ============================================================

def tinh_gpa(gpa_hien_tai, tin_chi_da_hoc):

    # --------------------------------------------------------
    # Kiểm tra dữ liệu
    # --------------------------------------------------------

    if tin_chi_da_hoc <= 0:
        return (
            "⚠️ Vui lòng nhập số tín chỉ đã học lớn hơn 0.",
            "",
            "",
            "",
            "",
            ""
        )

    if tin_chi_da_hoc >= TONG_TIN_CHI:
        return (
            "⚠️ Số tín chỉ đã học phải nhỏ hơn 137 tín chỉ.",
            "",
            "",
            "",
            "",
            ""
        )

    # --------------------------------------------------------
    # Tính số tín chỉ còn lại
    # --------------------------------------------------------

    tin_chi_con_lai = TONG_TIN_CHI - tin_chi_da_hoc

    # Khóa luận 9 tín chỉ được tính riêng
    tin_chi_mon_thuong = tin_chi_con_lai - TIN_CHI_KHOA_LUAN

    # Nếu còn chưa đủ 9 tín chỉ cho khóa luận
    if tin_chi_mon_thuong < 0:
        return (
            f"""
            <div class="canh-bao">
                ⚠️ Số tín chỉ đã học hiện tại là
                <b>{tin_chi_da_hoc}</b>.

                Theo giả định của chương trình, còn phải hoàn thành
                <b>{tin_chi_con_lai}</b> tín chỉ, trong đó khóa luận
                chiếm <b>9 tín chỉ</b>.
            </div>
            """,
            "",
            "",
            "",
            "",
            ""
        )

    # --------------------------------------------------------
    # Số môn 3 tín chỉ còn lại
    # --------------------------------------------------------

    so_mon_con_lai = tin_chi_mon_thuong // TIN_CHI_MON
    tin_chi_le = tin_chi_mon_thuong % TIN_CHI_MON

    # --------------------------------------------------------
    # GPA hiện tại -> tổng điểm tích lũy hiện tại
    # --------------------------------------------------------

    tong_diem_hien_tai = gpa_hien_tai * tin_chi_da_hoc

    # Tổng điểm cần có để GPA cuối cùng = 3.8
    tong_diem_muc_tieu = GPA_MUC_TIEU * TONG_TIN_CHI

    # Điểm khóa luận giả định A
    diem_khoa_luan = DIEM_KHOA_LUAN * TIN_CHI_KHOA_LUAN

    # Điểm cần đạt từ các môn 3 tín chỉ
    diem_can_tu_mon = (
        tong_diem_muc_tieu
        - tong_diem_hien_tai
        - diem_khoa_luan
    )

    # --------------------------------------------------------
    # Nếu còn tín chỉ lẻ
    # --------------------------------------------------------

    ghi_chu_tin_chi = ""

    if tin_chi_le != 0:
        ghi_chu_tin_chi = f"""
        <div class="canh-bao">
            ⚠️ Sau khi dành 9 tín chỉ cho khóa luận,
            còn <b>{tin_chi_le} tín chỉ</b> không phải bội số của
            3 tín chỉ/môn.

            Vì vậy phần tính B/C bên dưới chỉ xét các học phần
            3 tín chỉ.
        </div>
        """

    # --------------------------------------------------------
    # Tìm tất cả tổ hợp B/C
    #
    # Các môn không phải B/C được hiểu là A.
    # --------------------------------------------------------

    cac_to_hop = []

    for so_b in range(so_mon_con_lai + 1):

        for so_c in range(so_mon_con_lai - so_b + 1):

            so_a = so_mon_con_lai - so_b - so_c

            # Tổng điểm các môn 3 tín chỉ
            diem_cac_mon = (
                so_a * 4
                + so_b * 3
                + so_c * 2
            ) * TIN_CHI_MON

            tong_diem_cuoi = (
                tong_diem_hien_tai
                + diem_cac_mon
                + diem_khoa_luan
            )

            gpa_cuoi = tong_diem_cuoi / TONG_TIN_CHI

            if gpa_cuoi >= GPA_MUC_TIEU - 1e-9:

                cac_to_hop.append({
                    "a": so_a,
                    "b": so_b,
                    "c": so_c,
                    "gpa": gpa_cuoi
                })

    # --------------------------------------------------------
    # Kiểm tra khả năng đạt 3.8
    # --------------------------------------------------------

    gpa_toi_da = (
        tong_diem_hien_tai
        + so_mon_con_lai * TIN_CHI_MON * 4
        + diem_khoa_luan
    ) / TONG_TIN_CHI

    if not cac_to_hop:

        thong_bao = f"""
        <div class="khong-the">

            <div style="font-size: 42px;">😟</div>

            <h2>Chưa có tổ hợp B/C nào phù hợp</h2>

            <p>
                Với GPA hiện tại <b>{gpa_hien_tai:.2f}</b>,
                ngay cả khi các học phần còn lại đều đạt A,
                GPA cuối khóa tối đa khoảng
                <b>{gpa_toi_da:.2f}</b>.
            </p>

        </div>

        {ghi_chu_tin_chi}
        """

        return (
            thong_bao,
            tao_the("A", "—", "Môn A tối đa", "#1976D2", "#E3F2FD"),
            tao_the("B", "—", "Môn B tối đa", "#F57C00", "#FFF3E0"),
            tao_the("C", "—", "Môn C tối đa", "#D32F2F", "#FFEBEE"),
            "Không có tổ hợp B/C đáp ứng GPA 3.8.",
            ""
        )

    # --------------------------------------------------------
    # Tìm số B tối đa và C tối đa
    # --------------------------------------------------------

    max_b = max(x["b"] for x in cac_to_hop)
    max_c = max(x["c"] for x in cac_to_hop)

    # Tìm tổ hợp có nhiều B/C nhất
    to_hop_tot = max(
        cac_to_hop,
        key=lambda x: (
            x["b"] + x["c"],
            x["b"],
            -x["c"]
        )
    )

    # --------------------------------------------------------
    # Tạo bảng các tổ hợp
    # --------------------------------------------------------

    # Sắp xếp:
    # nhiều B/C trước, ít C trước
    cac_to_hop.sort(
        key=lambda x: (
            -(x["b"] + x["c"]),
            x["c"],
            -x["b"]
        )
    )

    danh_sach = []

    for i, x in enumerate(cac_to_hop, 1):

        a = x["a"]
        b = x["b"]
        c = x["c"]

        # Tạo chuỗi minh họa
        parts = []

        if a > 0:
            parts.append(
                f'<span class="badge-a">{a}A</span>'
            )

        if b > 0:
            parts.append(
                f'<span class="badge-b">{b}B</span>'
            )

        if c > 0:
            parts.append(
                f'<span class="badge-c">{c}C</span>'
            )

        to_hop = " ".join(parts)

        danh_sach.append(
            f"""
            <div class="dong-to-hop">
                <span class="so-thu-tu">{i}</span>
                {to_hop}
                <span class="gpa-to-hop">
                    GPA ≈ {x["gpa"]:.3f}
                </span>
            </div>
            """
        )

    # Chỉ hiển thị tối đa 80 tổ hợp
    if len(danh_sach) > 80:
        danh_sach = danh_sach[:80]

        danh_sach.append(
            f"""
            <div class="ghi-chu">
                Đang hiển thị 80 tổ hợp đầu tiên
                trong tổng số {len(cac_to_hop)} tổ hợp phù hợp.
            </div>
            """
        )

    danh_sach_html = "".join(danh_sach)

    # --------------------------------------------------------
    # Tạo phần tổng quan
    # --------------------------------------------------------

    tong_quan = f"""
    <div class="thanh-cong">

        <div style="font-size: 42px;">🎯</div>

        <h2>Có thể đạt GPA 3.8!</h2>

        <div class="thong-ke">

            <div>
                <span class="nhan">GPA hiện tại</span>
                <strong>{gpa_hien_tai:.2f}</strong>
            </div>

            <div>
                <span class="nhan">Tín chỉ đã học</span>
                <strong>{tin_chi_da_hoc}</strong>
            </div>

            <div>
                <span class="nhan">Tín chỉ còn lại</span>
                <strong>{tin_chi_con_lai}</strong>
            </div>

            <div>
                <span class="nhan">Học phần 3 tín chỉ</span>
                <strong>{so_mon_con_lai}</strong>
            </div>

        </div>

        <p>
            Khóa luận <b>9 tín chỉ</b> được giả định đạt
            <span class="badge-a">A (4.0)</span>.
        </p>

    </div>

    {ghi_chu_tin_chi}
    """

    # --------------------------------------------------------
    # Các thẻ A/B/C
    # --------------------------------------------------------

    the_a = tao_the(
        "A",
        to_hop_tot["a"],
        "Các môn còn lại đạt A",
        "#1976D2",
        "#E3F2FD"
    )

    the_b = tao_the(
        "B",
        max_b,
        "Số môn B tối đa",
        "#F57C00",
        "#FFF3E0"
    )

    the_c = tao_the(
        "C",
        max_c,
        "Số môn C tối đa",
        "#D32F2F",
        "#FFEBEE"
    )

    # --------------------------------------------------------
    # Chú thích
    # --------------------------------------------------------

    chu_thich = """
    <div class="chu-thich">

        <h3>🎨 Cách đọc kết quả</h3>

        <div>
            <span class="badge-a">A</span>
            <span class="badge-b">B</span>
            <span class="badge-c">C</span>
        </div>

        <p>
            <b>A = 4.0</b> &nbsp; | &nbsp;
            <b>B = 3.0</b> &nbsp; | &nbsp;
            <b>C = 2.0</b>
        </p>

        <p>
            Ví dụ:
            <span class="badge-a">5A</span>
            <span class="badge-b">2B</span>
            <span class="badge-c">1C</span>
            nghĩa là 5 môn A, 2 môn B và 1 môn C.
        </p>

    </div>
    """

    return (
        tong_quan,
        the_a,
        the_b,
        the_c,
        danh_sach_html,
        chu_thich
    )


# ============================================================
# CSS
# ============================================================

css = """

.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
}

/* Tiêu đề */

.tieu-de {
    text-align: center;
    padding: 20px 10px 5px 10px;
}

.mo-ta {
    text-align: center;
    color: #667085;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 25px;
}

/* Nút */

button.primary {
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* Kết quả */

.thanh-cong {
    padding: 24px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #E8F5E9,
        #F1F8E9
    );
    border: 1px solid #A5D6A7;
    text-align: center;
    margin: 10px 0 20px 0;
}

.khong-the {
    padding: 24px;
    border-radius: 20px;
    background: #FFEBEE;
    border: 1px solid #EF9A9A;
    text-align: center;
}

.thong-ke {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 20px 0;
}

.thong-ke div {
    background: rgba(255,255,255,0.8);
    padding: 14px;
    border-radius: 14px;
}

.thong-ke .nhan {
    display: block;
    color: #667085;
    font-size: 12px;
    margin-bottom: 5px;
}

.thong-ke strong {
    font-size: 22px;
}

/* Thẻ A/B/C */

.badge-a,
.badge-b,
.badge-c {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 9px;
    font-weight: 800;
    margin: 2px;
}

.badge-a {
    color: #1565C0;
    background: #E3F2FD;
    border: 1px solid #90CAF9;
}

.badge-b {
    color: #E65100;
    background: #FFF3E0;
    border: 1px solid #FFCC80;
}

.badge-c {
    color: #C62828;
    background: #FFEBEE;
    border: 1px solid #EF9A9A;
}

/* Danh sách tổ hợp */

.dong-to-hop {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 12px;
    margin: 5px 0;
    border-radius: 10px;
    background: #F8FAFC;
    border: 1px solid #EAECF0;
}

.so-thu-tu {
    width: 28px;
    color: #667085;
    font-weight: 600;
}

.gpa-to-hop {
    margin-left: auto;
    color: #667085;
    font-size: 13px;
}

.ghi-chu {
    text-align: center;
    color: #667085;
    padding: 15px;
}

.chu-thich {
    padding: 20px;
    margin-top: 15px;
    border-radius: 16px;
    background: #F8FAFC;
    text-align: center;
}

/* Cảnh báo */

.canh-bao {
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 12px;
    background: #FFF8E1;
    border-left: 4px solid #FFB300;
    color: #5D4037;
}

/* Miễn trừ */

.mien-tru {
    margin-top: 30px;
    padding: 18px;
    border-top: 1px solid #E5E7EB;
    text-align: center;
    color: #667085;
    font-size: 13px;
    line-height: 1.6;
}


/* Responsive */

@media (max-width: 700px) {

    .thong-ke {
        grid-template-columns: repeat(2, 1fr);
    }

    .dong-to-hop {
        flex-wrap: wrap;
    }

    .gpa-to-hop {
        width: 100%;
        margin-left: 28px;
    }
}

"""


# ============================================================
# GIAO DIỆN GRADIO
# ============================================================

with gr.Blocks(
    title="Tính khả năng đạt GPA 3.8",
    css=css,
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="green",
        neutral_hue="slate"
    )
) as ung_dung:

    # --------------------------------------------------------
    # Tiêu đề
    # --------------------------------------------------------

    gr.Markdown(
        """
        <div class="tieu-de">

            <h1>🎓 GPA 3.8 — Bạn còn bao nhiêu "dư địa" cho B/C?</h1>

        </div>

        <div class="mo-ta">

            Công cụ dành cho sinh viên để ước tính số học phần
            có thể đạt <b>B</b> hoặc <b>C</b> mà vẫn giữ GPA cuối khóa
            từ <b>3.8 trở lên</b>.

        </div>
        """
    )

    # --------------------------------------------------------
    # Thông số chương trình
    # --------------------------------------------------------

    gr.Markdown("### 📚 Thông tin chương trình")

    with gr.Row():

        gr.Markdown(
            """
            <div class="canh-bao">

            🎓 <b>137 tín chỉ</b> để tốt nghiệp

            </div>
            """
        )

        gr.Markdown(
            """
            <div class="canh-bao">

            📖 Mỗi học phần: <b>3 tín chỉ</b>

            </div>
            """
        )

        gr.Markdown(
            """
            <div class="canh-bao">

            📝 Khóa luận: <b>9 tín chỉ</b>

            </div>
            """
        )

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    gr.Markdown("### 📌 Thông tin của bạn")

    with gr.Row():

        with gr.Column():

            gpa_hien_tai = gr.Slider(
                minimum=0,
                maximum=4,
                value=3.2,
                step=0.01,
                label="GPA hiện tại (thang 4)",
                info="Kéo thanh trượt với độ chính xác 0,01"
            )

        with gr.Column():

            tin_chi_da_hoc = gr.Number(
                value=60,
                minimum=1,
                maximum=136,
                precision=0,
                label="Số tín chỉ đã học",
                info="Nhập tổng số tín chỉ bạn đã hoàn thành"
            )

    nut_tinh = gr.Button(
        "🚀 Tính khả năng đạt GPA 3.8",
        variant="primary",
        size="lg"
    )

    # --------------------------------------------------------
    # Kết quả tổng quan
    # --------------------------------------------------------

    gr.Markdown("### 📊 Tổng quan")

    ket_qua_tong_quat = gr.HTML()

    # --------------------------------------------------------
    # Visual A/B/C
    # --------------------------------------------------------

    gr.Markdown(
        "### 🎨 Hình dung các mức điểm"
    )

    with gr.Row():

        the_a = gr.HTML()

        the_b = gr.HTML()

        the_c = gr.HTML()

    # --------------------------------------------------------
    # Chú thích
    # --------------------------------------------------------

    chu_thich = gr.HTML()

    # --------------------------------------------------------
    # Danh sách tổ hợp
    # --------------------------------------------------------

    gr.Markdown(
        """
        ### 🔎 Các tổ hợp B/C có thể đạt

        Các môn không xuất hiện trong tổ hợp B/C được giả định
        đạt <b>A (4.0)</b>. Khóa luận 9 tín chỉ cũng được giả định
        đạt A.
        """
    )

    cac_to_hop = gr.HTML(
        value="""
        <div style="
            text-align:center;
            padding:30px;
            color:#667085;
        ">
            Nhập thông tin và nhấn
            <b>“Tính khả năng đạt GPA 3.8”</b>
            để xem kết quả.
        </div>
        """
    )

    # --------------------------------------------------------
    # Miễn trừ trách nhiệm
    # --------------------------------------------------------

    gr.Markdown(
        """
        <div class="mien-tru">

        ⚠️ <b>Miễn trừ trách nhiệm:</b>
        Kết quả của công cụ này <b>chỉ mang tính tham khảo</b>.
        Phép tính dựa trên các giả định: chương trình gồm 137 tín chỉ,
        học phần thông thường 3 tín chỉ, khóa luận 9 tín chỉ và
        khóa luận được tính là A (4.0).
        Kết quả thực tế có thể khác tùy quy chế đào tạo,
        cách tính GPA và cấu trúc học phần của trường.

        </div>
        """
    )

    # --------------------------------------------------------
    # Sự kiện
    # --------------------------------------------------------

    nut_tinh.click(
        fn=tinh_gpa,
        inputs=[
            gpa_hien_tai,
            tin_chi_da_hoc
        ],
        outputs=[
            ket_qua_tong_quat,
            the_a,
            the_b,
            the_c,
            cac_to_hop,
            chu_thich
        ]
    )


# ============================================================
# CHẠY ỨNG DỤNG
# ============================================================

ung_dung.launch(
    share=True
)
