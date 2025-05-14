export async function GET(req) {
    const { searchParams } = new URL(req.url);
    const userID = searchParams.get('userID');
    const timestamp = searchParams.get('timestamp');
  
    return Response.json({
      videoUrl: `https://example.com/processed/${userID}/${timestamp}_annotated.mp4`,
      analysis: {
        swingPathAngle: 7.5,
        clubfaceAngleAtImpact: 2.1,
        shoulderRotation: 45.0,
      },
    });
  }