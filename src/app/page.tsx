'use client';

import { useState } from 'react';

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  type ResultType = {
    videoUrl: string;
    analysis: {
      swingPathAngle: number;
      clubfaceAngleAtImpact: number;
      shoulderRotation: number;
    };
  };
  const [result, setResult] = useState<ResultType | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    const uploadRes = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    const { userID, timestamp } = await uploadRes.json();

    setUploading(false);
    setProcessing(true);

    const intervalId = setInterval(async () => {
      const statusRes = await fetch(`/api/check-status?userID=${userID}&timestamp=${timestamp}`);
      const status = await statusRes.json();

      if (status.status === 'completed') {
        clearInterval(intervalId);
        const resultRes = await fetch(`/api/get-result?userID=${userID}&timestamp=${timestamp}`);
        const resultData = await resultRes.json();
        setResult(resultData);
        setProcessing(false);
      }
    }, 5000);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-[#141414]">
      <h1 className="text-4xl font-bold mb-8">Golf Swing Analyzer</h1>

      {!uploading && !processing && !result && (
        <div className="flex flex-col items-center space-y-4">
          <input
            type="file"
            accept="video/*"
            onChange={(e) => {
              const fileList = e.target.files;
              if (fileList && fileList.length > 0) {
                setFile(fileList[0]);
              }
            }}
            className="border rounded p-2"
          />
          <button
            onClick={handleUpload}
            className="px-6 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded"
          >
            Upload Swing
          </button>
        </div>
      )}

      {uploading && <p className="text-lg text-blue-500">Uploading your swing...</p>}

      {processing && <p className="text-lg text-yellow-500">Analyzing your swing...</p>}

      {result && (
        <div className="flex flex-col items-center mt-8 space-y-4">
          <h2 className="text-2xl font-bold">Analysis Complete!</h2>
          <video controls className="w-full max-w-2xl rounded shadow">
            <source src={result.videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <div className="bg-white p-4 rounded shadow w-full max-w-md">
            <p><strong>Swing Path Angle:</strong> {result.analysis.swingPathAngle}°</p>
            <p><strong>Clubface Angle at Impact:</strong> {result.analysis.clubfaceAngleAtImpact}°</p>
            <p><strong>Shoulder Rotation:</strong> {result.analysis.shoulderRotation}°</p>
          </div>
        </div>
      )}
    </main>
  );
}
