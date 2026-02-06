export async function uploadFiles(files) {
    const formData=new FormData();
    for(let file of files){
        formData.append("files",file);
    }
    const response = await fetch("http://127.0.0.1:8000/upload", {
    method: "POST",
    body: formData,
  });
  if(!response.ok){
    throw new Error("Upload Failed....");
  }
  return response.json()
}
