import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [translation, setTranslation] = useState("");
  const [imgSrc, setImgSrc] = useState(null);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    const imgUrl = URL.createObjectURL(file);
    setImgSrc(imgUrl);
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setTranslation(data.translation);
  };

  useEffect(() => {
    return () => {
      if (imgSrc) {
        URL.revokeObjectURL(imgSrc);
      }
    };
  }, [imgSrc]);

  return (
    <div>
      <input type="file" onChange={handleUpload} />
      {imgSrc && (
        <img
          src={imgSrc}
          alt="Uploaded img"
          style={{ maxWidth: "100%", maxHeight: "400px" }}
        />
      )}
      <p>Translation: {translation}</p>
    </div>
  );
}

export default App;
