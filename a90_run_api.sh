BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

nohup python a08_muti_agents_gradio.py < /dev/null >> predict-api.log 2>&1 &
tail -f predict-api.log
