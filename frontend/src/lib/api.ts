const BACKEND_URL = process.env.BACKEND_URL || 'https://forge-media-backend.onrender.com';

export async function fetchDashboardData() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/dashboard`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch dashboard data');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return null;
  }
}

export async function uploadFile(file: File) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${BACKEND_URL}/api/files/upload`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Failed to upload file');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error uploading file:', error);
    return null;
  }
}
