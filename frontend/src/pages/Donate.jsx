import { useState } from "react";
import axios from "axios";

const Donate = () => {
    const [formData, setFormData] = useState({
        campaign_id: "",
        phone: "",
        amount: ""
    });
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleDonate = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/donations/donate/", formData);
            setMessage(response.data.message);
        } catch (err) {
            setError("Failed to initiate donation. Please try again.");
        }
        setLoading(false);
    };

    return (
        <div style={{ maxWidth: "400px", margin: "100px auto", padding: "20px" }}>
            <h2>Make a Donation</h2>
            <p>Enter your details below and you will receive an M-Pesa prompt on your phone.</p>
            {message && <p style={{ color: "green" }}>{message}</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleDonate}>
                <div style={{ marginBottom: "15px" }}>
                    <input
                        type="number"
                        name="campaign_id"
                        placeholder="Campaign ID"
                        value={formData.campaign_id}
                        onChange={handleChange}
                        style={{ width: "100%", padding: "10px" }}
                    />
                </div>
                <div style={{ marginBottom: "15px" }}>
                    <input
                        type="text"
                        name="phone"
                        placeholder="Phone e.g 254712345678"
                        value={formData.phone}
                        onChange={handleChange}
                        style={{ width: "100%", padding: "10px" }}
                    />
                </div>
                <div style={{ marginBottom: "15px" }}>
                    <input
                        type="number"
                        name="amount"
                        placeholder="Amount (KES)"
                        value={formData.amount}
                        onChange={handleChange}
                        style={{ width: "100%", padding: "10px" }}
                    />
                </div>
                <button
                    type="submit"
                    disabled={loading}
                    style={{ width: "100%", padding: "10px", backgroundColor: "#008000", color: "white", border: "none", cursor: "pointer" }}
                >
                    {loading ? "Processing..." : "Donate Now"}
                </button>
            </form>
        </div>
    );
};

export default Donate;