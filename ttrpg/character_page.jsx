// import React, { useState, useEffect } from "react";

// export default function character_page({ url }) {
//   const [newText, setNewText] = useState("");

//   function handleAddText(event) {
//     if (event.key === "Enter" && newText.trim()) {
//       event.preventDefault();
//       fetch(`/api/v1/characters/?characterid=${characterid}`, {
//         method: "POST",
//         credentials: "same-origin",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ text: newText }),
//       })
//         .then((response) => response.json())
//         .then((data) => {
//           setTexts([...texts, data]); // Adds new text
//           setNewText("");
//         })
//         .catch((error) => console.log(error));
//     }
//   }
// }

// broken code ^^
