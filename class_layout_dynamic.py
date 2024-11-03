import streamlit as stimport randomimport matplotlib.pyplot as pltimport numpy as npimport matplotlib.patches as patchesfrom fpdf import FPDFimport io# Set up the Streamlit app titlest.title("Dynamic Classroom Layout Generator")# Number of tables inputnum_tables = st.number_input('Enter the number of tables:', min_value=1, max_value=20, value=7)# Dynamically input number of students per tabletable_sizes = []for i in range(num_tables):    table_size = st.number_input(f"Number of students at Table {i + 1}:", min_value=1, max_value=6, value=3)    table_sizes.append(table_size)# Check if user input is validtotal_students_needed = sum(table_sizes)st.write(f"Total number of students: {total_students_needed}")# Get comma-separated student namesstudent_input = st.text_area("Enter student names separated by commas:", placeholder="e.g., Alice, Bob, Charlie")# Generate layout only if the number of students matches the input requirementsif st.button("Generate Classroom Layout"):    students = [name.strip() for name in student_input.split(",") if name.strip()]        if len(students) < total_students_needed:        st.error(f"Not enough students. You need at least {total_students_needed} students, but you entered {len(students)}.")    else:        # Shuffle students for randomness        random.shuffle(students)        # Create tables based on specified sizes        tables = []        index = 0        for size in table_sizes:            table = students[index:index + size]            tables.append(table)            index += size        # Draw the layout        fig, ax = plt.subplots(figsize=(10, 10))        ax.set_xlim(0, 15)        ax.set_ylim(0, 15)        ax.axis("off")        # Add whiteboard at the front of the room        whiteboard = patches.Rectangle((1, 14), 13, 0.3, linewidth=1, edgecolor="black", facecolor="lightgray")        ax.add_patch(whiteboard)        ax.text(7.5, 14.2, "Whiteboard", ha="center", va="center", fontsize=10, weight="bold")        # Place the teacher's desk on the right side of the room        teacher_desk = patches.Rectangle((12, 10.5), 1.5, 0.7, linewidth=1, edgecolor="black", facecolor="tab:orange", alpha=0.4)        ax.add_patch(teacher_desk)        ax.text(12.75, 10.85, "Teacher's Desk", ha="center", va="center", fontsize=10, weight="bold")        # Parameters for positioning student tables in three columns        table_positions = [(2, 12), (2, 9), (2, 6), (7, 12), (7, 9), (12, 6), (12, 3)]  # Predefined positions        if len(table_positions) < num_tables:            st.warning("You have more tables than predefined positions, some will overlap.")        table_width, table_height = 1.5, 0.7  # Width and height for the rectangle tables        chair_offset_x, chair_offset_y = table_width / 2 + 0.5, table_height / 2 + 0.5        # Draw each table with chairs        for i, (table, position) in enumerate(zip(tables, table_positions)):            x, y = position            rect = patches.Rectangle((x - table_width / 2, y - table_height / 2),                                     table_width, table_height, linewidth=1,                                     edgecolor="black", facecolor="tab:blue", alpha=0.3)            ax.add_patch(rect)            ax.text(x, y, f"Table {i + 1}", ha="center", va="center", fontsize=12, weight="bold", color="black")            for j, student in enumerate(table):                if len(table) == 3:                    angles = [0, 120, 240]                    chair_x = x + chair_offset_x * np.cos(np.radians(angles[j]))                    chair_y = y + chair_offset_y * np.sin(np.radians(angles[j]))                elif len(table) == 2:                    chair_x, chair_y = (x - chair_offset_x, y) if j == 0 else (x + chair_offset_x, y)                else:                    chair_x = x + (chair_offset_x if j % 2 else -chair_offset_x)                    chair_y = y + (chair_offset_y if j < 2 else -chair_offset_y)                ax.plot(chair_x, chair_y, marker="o", markersize=30, color="tab:green", alpha=0.7)                ax.text(chair_x, chair_y, student, ha="center", va="center", fontsize=8, color="white")        st.pyplot(fig)        # Option to download as PDF        if st.button("Download Layout as PDF"):            pdf = FPDF()            pdf.add_page()            pdf.set_font("Arial", size=12)            pdf.cell(200, 10, txt="Classroom Layout", ln=True, align="C")            # Save each table's layout to the PDF            for i, table in enumerate(tables):                pdf.cell(200, 10, txt=f"Table {i + 1}: {', '.join(table)}", ln=True)            # Save PDF to a buffer            pdf_output = io.BytesIO()            pdf.output(pdf_output)            pdf_output.seek(0)            # Provide download link            st.download_button(label="Download PDF", data=pdf_output, file_name="classroom_layout.pdf", mime="application/pdf")