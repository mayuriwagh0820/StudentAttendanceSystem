const students = [];
const attendance = [];

const studentForm = document.getElementById("studentForm");
const studentList = document.getElementById("studentList");
const attendanceRecords = document.getElementById("attendanceRecords");
const attendanceDate = document.getElementById("attendanceDate");
const message = document.getElementById("message");

attendanceDate.value = new Date().toLocaleDateString("en-CA");

studentForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("studentName").value.trim();
    const roll = document.getElementById("studentRoll").value.trim();

    if (!name || !roll) return;

    if (students.some(student => student.roll === roll)) {
        message.textContent = "That roll number already exists.";
        return;
    }

    students.push({ name, roll });
    studentForm.reset();
    message.textContent = "Student added successfully.";
    renderStudents();
});

function renderStudents() {
    studentList.replaceChildren();

    if (students.length === 0) {
        studentList.textContent = "Add a student to begin.";
        return;
    }

    students.forEach(student => {
        const row = document.createElement("div");
        row.className = "student-row";

        const label = document.createElement("label");
        label.textContent = `${student.roll} - ${student.name}: `;

        const select = document.createElement("select");
        select.dataset.roll = student.roll;

        ["Present", "Absent"].forEach(status => {
            const option = document.createElement("option");
            option.value = status;
            option.textContent = status;
            select.appendChild(option);
        });

        label.appendChild(select);
        row.appendChild(label);
        studentList.appendChild(row);
    });
}

document.getElementById("saveAttendance").addEventListener("click", function () {
    const date = attendanceDate.value;

    if (!date) {
        message.textContent = "Please select an attendance date.";
        return;
    }

    if (students.length === 0) {
        message.textContent = "Please add students first.";
        return;
    }

    const selections = [...studentList.querySelectorAll("select")];

    selections.forEach(select => {
        const record = {
            date,
            roll: select.dataset.roll,
            status: select.value
        };

        const existing = attendance.find(item =>
            item.date === record.date && item.roll === record.roll
        );

        if (existing) {
            existing.status = record.status;
        } else {
            attendance.push(record);
        }
    });

    message.textContent = "Attendance saved successfully.";
    renderRecords();
});

function renderRecords() {
    attendanceRecords.replaceChildren();

    if (attendance.length === 0) {
        attendanceRecords.textContent = "No attendance records yet.";
        return;
    }

    attendance.forEach(record => {
        const student = students.find(item => item.roll === record.roll);
        const row = document.createElement("div");
        row.className = "record-row";
        row.textContent =
            `${record.date} | ${record.roll} - ${student ? student.name : "Unknown"} | ${record.status}`;
        attendanceRecords.appendChild(row);
    });
}

renderStudents();
renderRecords();
