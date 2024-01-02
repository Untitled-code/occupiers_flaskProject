#!/bin/bash
# File paths
#input_file="orks__test.txt"
#input_file="test.txt"
input_file="test2.txt"
output_file="output.csv"

# Initialize the output file with headers
echo "FIO,DOB,Position,Unit,Passport,Passport_Issue_Date,Issued_By,Taxpayer_Number,Social_Security_Number,Address,Phone_Number,Social_Media,Email,Status,Verified,Source,Image_File" > "$output_file"

# Process the input file and append to the output file
awk '
BEGIN { RS = ""; FS = "\n" }

{
    delete values;
    image_file = "nopicture.jpeg"; # Default image file;
    for (i = 1; i <= NF; i++) {
        if ($i ~ /\.jpg$/) {
            image_file = $i;
            continue;
        }
        # Replace all '/ч' with ''
        { gsub("/ч", "ч"); }

        # Replace all '_' with '-'
        { gsub("_", "-"); }

        if ($i ~ /: /) {
            split($i, kv, ": ");
            key = kv[1];
            value = kv[2];
            gsub(/^[ \t]+|[ \t]+$/, "", key);
            gsub(/^[ \t]+|[ \t]+$/, "", value);
            if (key == "ФИО") key = "FIO";
            else if (key == "ДР") key = "DOB";
            else if (key == "Должность") key = "Position";
            else if (key == "Войсковая часть") key = "Unit";
            else if (key == "Паспорт") key = "Passport";
            else if (key == "Дата паспорта") key = "Passport_Issue_Date";
            else if (key == "Кем выдан") key = "Issued_Bpy";
            else if (key == "ИНН") key = "Taxpayer_Number";
            else if (key == "СНИЛС") key = "Social_Security_Number";
            else if (key == "Адрес") key = "Address";
            else if (key == "Телефон") key = "Phone_Number";
            else if (key == "Соцсети") key = "Social_Media";
            else if (key == "Email") key = "Email";
            else if (key == "Статус") key = "Status";
            else if (key == "Верифицировано") key = "Verified";
            else if (key == "Джерело") key = "Source";
            values[key] = value;
        }
    }
    printf "\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n",
           values["FIO"], values["DOB"], values["Position"], values["Unit"], values["Passport"], values["Passport_Issue_Date"],
           values["Issued_By"], values["Taxpayer_Number"], values["Social_Security_Number"], values["Address"], values["Phone_Number"],
           values["Social_Media"], values["Email"], values["Status"], values["Verified"], values["Source"], image_file
}' "$input_file" >> "$output_file"