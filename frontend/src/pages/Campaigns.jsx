import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

const Campaigns = () => {
    const [campaigns, setCampaigns] = useState([]);
    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        target_amount: "",
        deadline: ""
    });
    const [showForm, setShowForm] = useState(false);
    const { token } = useAuth();

    const fetchCampaigns = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/campaigns/", {
                headers: { Authorization: `Bearer ${token}` }
            });
            setCampaigns(response.data);
        } catch (err) {
            setError("Failed to load campaigns");
        }
    };

    useEffect(() => {
        fetchCampaigns();
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://127.0.0.1:8000/api/campaigns/", formData, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setShowForm(false);
            fetchCampaigns();
        } catch (err) {
            setError("Failed to create campaign");
        }
    };

    return (
        <div style={{ maxWidth: "800px", margin: "50px auto", padding: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h2>My Campaigns</h2>
                <button
                    onClick={() => setShowForm(!showForm)}
                    style={{ padding: "10px 20px", backgroundColor: "#008000", color: "white", border: "none", cursor: "pointer" }}
                >
                    {showForm ? "Cancel" : "Create Campaign"}
                </button>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {showForm && (
                <form onSubmit={handleCreate} style={{ marginTop: "20px", padding: "20px", border: "1px solid #ccc" }}>
                    <h3>New Campaign</h3>
                    <div style={{ marginBottom: "15px" }}>
                        <input
                            type="text"
                            name="title"
                            placeholder="Campaign Title"
                            value={formData.title}
                            onChange={handleChange}
                            style={{ width: "100%", padding: "10px" }}
                        />
                    </div>
                    <div style={{ marginBottom: "15px" }}>
                        <textarea
                            name="description"
                            placeholder="Description"
                            value={formData.description}
                            onChange={handleChange}
                            style={{ width: "100%", padding: "10px", height: "100px" }}
                        />
                    </div>
                    <div style={{ marginBottom: "15px" }}>
                        <input
                            type="number"
                            name="target_amount"
                            placeholder="Target Amount (KES)"
                            value={formData.target_amount}
                            onChange={handleChange}
                            style={{ width: "100%", padding: "10px" }}
                        />
                    </div>
                    <div style={{ marginBottom: "15px" }}>
                        <input
                            type="date"
                            name="deadline"
                            value={formData.deadline}
                            onChange={handleChange}
                            style={{ width: "100%", padding: "10px" }}
                        />
                    </div>
                    <button type="submit" style={{ width: "100%", padding: "10px", backgroundColor: "#008000", color: "white" }}>
                        Create Campaign
                    </button>
                </form>
            )}

            <div style={{ marginTop: "30px" }}>
                {campaigns.length === 0 ? (
                    <p>No campaigns yet. Create your first one!</p>
                ) : (
                    campaigns.map((campaign) => (
                        <div key={campaign.id} style={{ padding: "20px", border: "1px solid #ccc", marginBottom: "15px", borderRadius: "5px" }}>
                            <h3>{campaign.title}</h3>
                            <p>{campaign.description}</p>
                            <p>Target: KES {campaign.target_amount}</p>
                            <p>Raised: KES {campaign.amount_raised}</p>
                            <p>Deadline: {campaign.deadline}</p>
                            <p>Status: <strong>{campaign.status}</strong></p>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Campaigns;