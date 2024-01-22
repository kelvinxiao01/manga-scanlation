import React, { useState } from "react";
import "./App.css";

function App() {
  const [translation, setTranslation] = useState("");

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setTranslation(data.translation);
  };

  return (
    <div>
      <input type="file" onChange={handleUpload} />
      <p>Translation: {translation}</p>
    </div>
  );
}

export default App;
