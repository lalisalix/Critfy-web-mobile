const baseUrl = 'http://127.0.0.1:8000/api';


function fetchAlbums() {
  fetch(`${baseUrl}/albums/`, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('access_token')}`
    }
  })
    .then(response => response.json())
    .then(data => {
      const albumList = document.getElementById('albumList');
      albumList.innerHTML = '';
      data.forEach(album => {
        const li = document.createElement('li');
        li.innerHTML = `
          <strong>${album.name}</strong> - ${album.artist} (${album.release_date})
          <button onclick="editAlbum(${album.id})">Editar</button>
          <button onclick="deleteAlbum(${album.id})">Excluir</button>
        `;
        albumList.appendChild(li);
      });
    });
}


function saveAlbum(event) {
  event.preventDefault();
  const id = document.getElementById('albumId').value;
  const name = document.getElementById('name').value;
  const artist = document.getElementById('artist').value;
  const releaseDate = document.getElementById('releaseDate').value;

  const method = id ? 'PUT' : 'POST';
  const url = id ? `${baseUrl}/albums/${id}/` : `${baseUrl}/albums/`;

  fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify({ name, artist, release_date: releaseDate })
  })
    .then(() => {
      fetchAlbums();
      document.getElementById('albumForm').reset();
    });
}

function editAlbum(id) {
  fetch(`${baseUrl}/albums/${id}/`, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('access_token')}`
    }
  })
    .then(response => response.json())
    .then(album => {
      document.getElementById('albumId').value = album.id;
      document.getElementById('name').value = album.name;
      document.getElementById('artist').value = album.artist;
      document.getElementById('releaseDate').value = album.release_date;
    });
}

function deleteAlbum(id) {
  fetch(`${baseUrl}/albums/${id}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Token ${localStorage.getItem('access_token')}`
    }
  })
    .then(() => fetchAlbums());
}

document.getElementById('albumForm').addEventListener('submit', saveAlbum);
fetchAlbums();
