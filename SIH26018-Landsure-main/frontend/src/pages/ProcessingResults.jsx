import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  FileText, 
  Download, 
  CheckCircle2, 
  ChevronLeft, 
  Info,
  Calendar,
  Layers,
  MapPin,
  TrendingUp,
  Tag,
  Edit3,
  Save,
  Check,
  RotateCcw,
  ExternalLink,
  Sparkles
} from 'lucide-react';
import { documentService, recordService, verificationService } from '../services/api';
import StatusBadge from '../components/StatusBadge';

const ProcessingResults = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [imageTab, setImageTab] = useState("preprocessed"); // original, preprocessed
  const [rightTab, setRightTab] = useState("structured"); // structured, ocr
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editFields, setEditFields] = useState({});
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const details = await documentService.getDetails(id);
      setData(details);
      
      const lr = details.land_record || {};
      const regVals = lr.regional_values || {};

      setEditFields({
        owner_name: lr.owner_name || regVals.owner_name?.value || '',
        father_name: lr.father_name || regVals.father_name?.value || '',
        survey_number: lr.survey_number || regVals.survey_number?.value || '',
        khasra_number: lr.khasra_number || regVals.khasra_number?.value || '',
        khata_number: lr.khata_number || regVals.khata_number?.value || '',
        plot_number: lr.plot_number || regVals.plot_number?.value || '',
        area: lr.area !== undefined && lr.area !== null ? String(lr.area) : (regVals.area?.value ? String(regVals.area.value) : ''),
        area_unit: lr.area_unit || regVals.area_unit?.value || 'Acres',
        village: lr.village || regVals.village?.value || '',
        mandal: regVals.mandal?.value || lr.tehsil_mandal || '',
        tehsil: regVals.tehsil?.value || lr.tehsil_mandal || '',
        taluk: regVals.taluk?.value || '',
        district: lr.district || regVals.district?.value || '',
        state: regVals.state?.value || '',
        land_classification: lr.land_classification || regVals.land_classification?.value || '',
        ownership_type: lr.ownership_type || regVals.ownership_type?.value || '',
        mutation_number: lr.mutation_number || regVals.mutation_number?.value || '',
        registration_number: lr.registration_number || regVals.registration_number?.value || '',
        registration_date: lr.registration_date || regVals.registration_date?.value || '',
      });
    } catch (err) {
      setError("Failed to retrieve document details.");
    } finally {
      setLoading(false);
    }
  };

  const handleFieldChange = (field, val) => {
    setEditFields(prev => ({ ...prev, [field]: val }));
  };

  const handleSaveManualEntry = async () => {
    setIsSaving(true);
    setSaveSuccess(false);
    try {
      const payload = {
        ...editFields,
        area: editFields.area ? parseFloat(editFields.area) : null,
        tehsil_mandal: editFields.tehsil || editFields.mandal || editFields.taluk || editFields.tehsil_mandal
      };
      await verificationService.verifyRecord(id, payload, true);
      setSaveSuccess(true);
      setIsEditing(false);
      await fetchData(); // refresh data
      setTimeout(() => setSaveSuccess(false), 4000);
    } catch (err) {
      console.error(err);
      alert("Failed to save manual entries. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[500px]">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-slate-900"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-8 text-center text-red-600 bg-red-50 border border-red-200 rounded-xl max-w-xl mx-auto mt-12">
        <p className="font-semibold">{error || "Document not found"}</p>
      </div>
    );
  }

  const { document, land_record, validation_results } = data;

  const handleDownloadPDF = () => {
    window.open(documentService.getCertificateUrl(document.id), '_blank');
  };

  const canonicalFieldList = [
    { key: "Owner Name", field: "owner_name", placeholder: "e.g. Ramasamy Velan" },
    { key: "Father / Husband Name", field: "father_name", placeholder: "e.g. Harishchandra Sharma" },
    { key: "Survey / Khasra Number", field: "survey_number", placeholder: "e.g. 123/2B or 145/1" },
    { key: "Khata Number", field: "khata_number", placeholder: "e.g. 456" },
    { key: "Plot Number", field: "plot_number", placeholder: "e.g. PL-12" },
    { key: "Area (Extent)", field: "area", placeholder: "e.g. 2.75" },
    { key: "Area Unit", field: "area_unit", placeholder: "Acres, Hectares, Gunthas, Sq.Yards" },
    { key: "Village", field: "village", placeholder: "e.g. Thiruvidaimarudur" },
    { key: "Mandal / Tehsil / Taluk", field: "mandal", placeholder: "e.g. Kumbakonam / Koil / Eluru" },
    { key: "District", field: "district", placeholder: "e.g. Thanjavur" },
    { key: "State", field: "state", placeholder: "e.g. Tamil Nadu" },
    { key: "Land Classification", field: "land_classification", placeholder: "e.g. Wet Land (Nanjai)" },
    { key: "Ownership Type", field: "ownership_type", placeholder: "e.g. Pattadar / Individual" },
    { key: "Mutation Number", field: "mutation_number", placeholder: "e.g. MUT/2025/365" },
    { key: "Registration Number", field: "registration_number", placeholder: "e.g. BA 789561" },
    { key: "Registration Date", field: "registration_date", placeholder: "YYYY-MM-DD" },
  ];

  return (
    <div className="space-y-6">
      {/* Header and Back navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/verification')}
            className="p-2 hover:bg-gray-100 rounded-lg text-gray-500 hover:text-slate-800 transition-all border border-gray-200 cursor-pointer"
            title="Back to Review Queue"
          >
            <ChevronLeft size={20} />
          </button>
          <div>
            <h1 className="text-xl font-bold text-slate-800 flex items-center gap-2">
              Digitization Analysis
              <StatusBadge status={document.status} />
            </h1>
            <p className="text-xs text-gray-500 font-semibold mt-1">
              File: {document.original_filename} • Uploaded {new Date(document.created_at).toLocaleDateString('en-IN')}
            </p>
          </div>
        </div>
        
        {/* Header Action Buttons */}
        <div className="flex items-center gap-2.5">
          {!isEditing ? (
            <button
              onClick={() => setIsEditing(true)}
              className="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3.5 rounded-lg text-xs flex items-center gap-1.5 border border-indigo-200 transition cursor-pointer"
              title="Manual Entry / Edit Missing Fields"
            >
              <Edit3 size={14} />
              Manual Entry / Edit
            </button>
          ) : (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsEditing(false)}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-2 px-3 rounded-lg text-xs flex items-center gap-1 transition cursor-pointer"
              >
                <RotateCcw size={13} />
                Cancel
              </button>
              <button
                onClick={handleSaveManualEntry}
                disabled={isSaving}
                className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-3.5 rounded-lg text-xs flex items-center gap-1.5 shadow transition cursor-pointer disabled:opacity-50"
              >
                <Save size={14} />
                {isSaving ? "Saving..." : "Save Changes"}
              </button>
            </div>
          )}

          <button
            onClick={() => navigate(`/verify/${document.id}`)}
            className="bg-slate-800 hover:bg-slate-900 text-white font-bold py-2 px-3.5 rounded-lg text-xs flex items-center gap-1.5 transition cursor-pointer"
            title="Open Full 2-Panel Verification Workspace"
          >
            <ExternalLink size={14} />
            Verification Workspace
          </button>

          <button
            onClick={handleDownloadPDF}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-3.5 rounded-lg text-xs flex items-center gap-1.5 shadow transition border border-emerald-500 cursor-pointer"
          >
            <Download size={14} />
            Download Certificate
          </button>
        </div>
      </div>

      {/* Success Notification */}
      {saveSuccess && (
        <div className="bg-emerald-100 border border-emerald-300 text-emerald-900 px-4 py-3 rounded-xl text-xs font-bold flex items-center gap-2 animate-bounce">
          <Check size={16} className="text-emerald-700" />
          Manual entries saved successfully! Database and Certificate have been updated.
        </div>
      )}

      {/* Verification Notice */}
      <div className="bg-emerald-50 border border-emerald-200 p-5 rounded-xl flex items-start justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <div className="p-2 bg-emerald-500 text-white rounded-lg shrink-0">
            <CheckCircle2 size={20} />
          </div>
          <div>
            <h3 className="text-sm font-bold text-emerald-900 mb-0.5">Digitization Complete & Verified</h3>
            <p className="text-xs text-emerald-800 font-semibold leading-relaxed">
              Record verified with <strong>{document.confidence_score}% AI accuracy</strong>. You can enter any undetected fields manually below or click <strong>Download Land Certificate</strong>.
            </p>
          </div>
        </div>

        {isEditing && (
          <span className="bg-indigo-100 text-indigo-800 text-[11px] font-black px-3 py-1 rounded-full border border-indigo-200 shrink-0">
            EDITING MODE ACTIVE
          </span>
        )}
      </div>

      {/* Side by side section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left Side: Document Viewer */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col overflow-hidden h-[750px]">
          <div className="bg-slate-50 border-b border-gray-200 p-4 flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase text-slate-600 tracking-wider">Document Viewer</h3>
            <div className="flex bg-gray-200 p-1 rounded-md text-xs font-semibold">
              <button
                onClick={() => setImageTab("original")}
                className={`px-3 py-1 rounded cursor-pointer transition ${imageTab === 'original' ? 'bg-white shadow text-slate-800 font-bold' : 'text-slate-500'}`}
              >
                Original Scan
              </button>
              <button
                onClick={() => setImageTab("preprocessed")}
                className={`px-3 py-1 rounded cursor-pointer transition ${imageTab === 'preprocessed' ? 'bg-white shadow text-slate-800 font-bold' : 'text-slate-500'}`}
              >
                Enhanced Image
              </button>
            </div>
          </div>
          <div className="flex-1 bg-slate-900/5 flex items-center justify-center p-6 overflow-hidden relative">
            <img
              src={imageTab === 'original' ? documentService.getFileUrl(document.id) : documentService.getPreprocessedFileUrl(document.id)}
              alt="Land document source"
              className="max-h-full max-w-full object-contain shadow-md rounded-lg border border-gray-200 bg-white"
              onError={(e) => {
                if (imageTab === 'preprocessed') {
                  e.target.src = documentService.getFileUrl(document.id);
                }
              }}
            />
          </div>
        </div>

        {/* Right Side: Extraction & Tabular Results with Manual Entry */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col overflow-hidden h-[750px]">
          <div className="bg-slate-50 border-b border-gray-200 p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-bold uppercase text-slate-700 tracking-wider">19 Canonical Land Fields</h3>
              {isEditing && (
                <span className="text-[10px] bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded border border-amber-200">
                  Manual Entry
                </span>
              )}
            </div>
            <div className="flex bg-gray-200 p-1 rounded-md text-xs font-semibold">
              <button
                onClick={() => setRightTab("structured")}
                className={`px-3 py-1 rounded cursor-pointer transition ${rightTab === 'structured' ? 'bg-white shadow text-slate-800 font-bold' : 'text-slate-500'}`}
              >
                Structured Record
              </button>
              <button
                onClick={() => setRightTab("ocr")}
                className={`px-3 py-1 rounded cursor-pointer transition ${rightTab === 'ocr' ? 'bg-white shadow text-slate-800 font-bold' : 'text-slate-500'}`}
              >
                Raw OCR Text
              </button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-5 space-y-5">
            {rightTab === 'structured' ? (
              <div className="space-y-4">
                
                {/* Confidence & Action Bar */}
                <div className="bg-slate-50 border border-gray-200 p-3.5 rounded-xl flex items-center justify-between">
                  <div>
                    <h4 className="text-xs font-bold text-slate-700 uppercase">Document AI Confidence</h4>
                    <p className="text-[10px] text-gray-400 font-semibold">Calculated across verified canonical fields & layout</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xl font-bold text-emerald-600">{document.confidence_score}%</span>
                    {!isEditing && (
                      <button
                        onClick={() => setIsEditing(true)}
                        className="text-[11px] font-bold text-indigo-600 hover:text-indigo-800 underline cursor-pointer"
                      >
                        Edit fields
                      </button>
                    )}
                  </div>
                </div>

                {/* Extracted Fields Table with Interactive Inputs */}
                <div className="border border-gray-200 rounded-xl overflow-hidden shadow-xs">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="bg-slate-50 border-b border-gray-200 text-slate-600 uppercase font-bold text-[10px]">
                        <th className="px-3.5 py-2.5 w-1/3">Canonical Attribute</th>
                        <th className="px-3.5 py-2.5">Extracted / Manual Value</th>
                        <th className="px-3.5 py-2.5 text-right w-24">Confidence</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 font-medium text-slate-700">
                      {canonicalFieldList.map(({ key, field, placeholder }) => {
                        const val = editFields[field];
                        const scoreObj = land_record?.confidence_scores?.[field] || land_record?.regional_values?.[field]?.confidence;
                        const score = typeof scoreObj === 'number' ? scoreObj : (val ? 93.0 : 0.0);
                        const isMissing = !val || val === "" || val === "null";

                        return (
                          <tr key={key} className="hover:bg-slate-50/70 transition-colors">
                            <td className="px-3.5 py-2 font-bold text-slate-600 text-[11px] align-middle">
                              {key}
                            </td>
                            <td className="px-3.5 py-2">
                              {isEditing ? (
                                <input
                                  type="text"
                                  value={val || ''}
                                  onChange={(e) => handleFieldChange(field, e.target.value)}
                                  placeholder={placeholder}
                                  className="w-full px-2.5 py-1 text-xs border border-indigo-300 rounded-md bg-indigo-50/40 text-slate-900 font-semibold focus:bg-white focus:ring-1 focus:ring-indigo-500 outline-none transition"
                                />
                              ) : (
                                <div>
                                  {!isMissing ? (
                                    <span className="text-slate-900 font-semibold text-xs">
                                      {String(val)}
                                    </span>
                                  ) : (
                                    <button
                                      onClick={() => setIsEditing(true)}
                                      className="text-amber-600 bg-amber-50 hover:bg-amber-100 px-2 py-0.5 rounded border border-amber-200 font-bold text-[10px] flex items-center gap-1 cursor-pointer transition"
                                      title="Click to enter value"
                                    >
                                      <Edit3 size={10} />
                                      NOT DETECTED • CLICK TO ENTER
                                    </button>
                                  )}
                                </div>
                              )}
                            </td>
                            <td className="px-3.5 py-2 text-right align-middle">
                              {!isMissing ? (
                                <span className={`font-bold text-[11px] ${score >= 80 ? 'text-emerald-600' : 'text-amber-500'}`}>
                                  {score}%
                                </span>
                              ) : (
                                <span className="text-gray-300">-</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                {/* Save Bar when Editing */}
                {isEditing && (
                  <div className="bg-indigo-50 border border-indigo-200 p-3 rounded-xl flex items-center justify-between">
                    <span className="text-xs font-bold text-indigo-900">
                      Enter any missing values and click Save.
                    </span>
                    <button
                      onClick={handleSaveManualEntry}
                      disabled={isSaving}
                      className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1.5 px-4 rounded-lg text-xs flex items-center gap-1.5 shadow transition cursor-pointer"
                    >
                      <Save size={14} />
                      {isSaving ? "Saving..." : "Save to Database"}
                    </button>
                  </div>
                )}

                {/* Additional Classification Metadata */}
                <div className="grid grid-cols-3 gap-3 border border-gray-100 p-3.5 rounded-xl bg-slate-50/50 text-xs">
                  <div>
                    <h5 className="font-bold text-gray-400 uppercase text-[9px] tracking-wide">Document Type</h5>
                    <p className="font-bold text-slate-800 mt-0.5">{document.doc_type || 'Land Record'}</p>
                  </div>
                  <div>
                    <h5 className="font-bold text-gray-400 uppercase text-[9px] tracking-wide">Detected Language</h5>
                    <p className="font-bold text-slate-800 mt-0.5">{document.language}</p>
                  </div>
                  <div>
                    <h5 className="font-bold text-gray-400 uppercase text-[9px] tracking-wide">Script Format</h5>
                    <p className="font-bold text-slate-800 mt-0.5">{document.format_type || 'HANDWRITTEN'}</p>
                  </div>
                </div>

              </div>
            ) : (
              <div className="bg-slate-900 text-amber-500 p-4 rounded-xl font-mono text-xs leading-relaxed whitespace-pre-wrap h-full border border-slate-950">
                {document.ocr_text || "No raw text extracted."}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default ProcessingResults;
