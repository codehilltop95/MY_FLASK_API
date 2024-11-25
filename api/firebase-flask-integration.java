// Android/Java code
public class UserApiClient {
    private static final String API_BASE_URL = "http://your-flask-api-url.com";
    private OkHttpClient client = new OkHttpClient();
    private static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    
    public void sendUIDToServer(String uid, final ApiCallback callback) {
        // Create JSON body
        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("uid", uid);
            // Add any additional user data you want to send
            jsonBody.put("timestamp", System.currentTimeMillis());
        } catch (JSONException e) {
            callback.onFailure("Error creating JSON: " + e.getMessage());
            return;
        }

        // Create request
        Request request = new Request.Builder()
            .url(API_BASE_URL + "/user")
            .post(RequestBody.create(JSON, jsonBody.toString()))
            .build();

        // Execute request asynchronously
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                callback.onFailure("Network error: " + e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    callback.onSuccess(response.body().string());
                } else {
                    callback.onFailure("Server error: " + response.code());
                }
            }
        });
    }

    // Callback interface
    public interface ApiCallback {
        void onSuccess(String response);
        void onFailure(String error);
    }
}

// Usage in your Activity/Fragment
public class MainActivity extends AppCompatActivity {
    private UserApiClient apiClient = new UserApiClient();

    private void sendCurrentUserUID() {
        FirebaseUser currentUser = FirebaseAuth.getInstance().getCurrentUser();
        if (currentUser != null) {
            String uid = currentUser.getUid();
            apiClient.sendUIDToServer(uid, new UserApiClient.ApiCallback() {
                @Override
                public void onSuccess(String response) {
                    runOnUiThread(() -> {
                        Toast.makeText(MainActivity.this, 
                            "UID sent successfully", Toast.LENGTH_SHORT).show();
                    });
                }

                @Override
                public void onFailure(String error) {
                    runOnUiThread(() -> {
                        Toast.makeText(MainActivity.this, 
                            "Error: " + error, Toast.LENGTH_SHORT).show();
                    });
                }
            });
        } else {
            Toast.makeText(this, "No user is signed in", Toast.LENGTH_SHORT).show();
        }
    }
}
